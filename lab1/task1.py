import base64
import random
from time import sleep, time

import requests

from tqdm import tqdm


class MersenneTwist: 
  def __init__(self, seed: int):
    (self.w, self.n, self.m, self.r) = (32, 624, 397, 31)
    (self.a, self.u, self.d) = (0x9908B0DF, 11, 0xFFFFFFFF)
    (self.s, self.b) = (7, 0x9D2C5680)
    (self.t, self.c) = (15, 0xEFC60000)
    (self.l, self.f) = (18, 1812433253)

    self.MT = [0] * self.n
    self.index = self.n + 1
    self.lower_mask = (1 << self.r) - 1
    self.upper_mask = (~self.lower_mask) & 0xFFFFFFFF

    self.seed_mt(seed)

  def seed_mt(self, seed: int):
    self.index = self.n
    self.MT[0] = seed
    for i in range(1, self.n):
      self.MT[i] = (self.f * (self.MT[i - 1] ^ (self.MT[i - 1] >> (self.w - 2))) + i) & 0xFFFFFFFF

  def extract_number(self):
    if self.index >= self.n:
      if self.index > self.n:
        raise Exception("Generator was never seeded")
      self.twist()

    y = self.MT[self.index]
    y = y ^ ((y >> self.u) & self.d)
    y = y ^ ((y << self.s) & self.b)
    y = y ^ ((y << self.t) & self.c)
    y = y ^ (y >> self.l)
    self.index += 1
    return y & 0xFFFFFFFF

  def twist(self):
    for i in range(self.n):
      x = (self.MT[i] & self.upper_mask) + (self.MT[(i + 1) % self.n] & self.lower_mask)
      xA = x >> 1
      if x % 2 != 0:
        xA = xA ^ self.a
      self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
    self.index = 0


class MersenneTwist: 
  def __init__(self):
    (self.w, self.n, self.m, self.r) = (32, 624, 397, 31)
    (self.a, self.u, self.d) = (0x9908B0DF, 11, 0xFFFFFFFF)
    (self.s, self.b) = (7, 0x9D2C5680)
    (self.t, self.c) = (15, 0xEFC60000)
    (self.l, self.f) = (18, 1812433253)

    # self.MT = [0] * self.n
    self.index = self.n + 1
    self.lower_mask = (1 << self.r) - 1
    self.upper_mask = (~self.lower_mask) & 0xFFFFFFFF

  def unmix(self, extractedNum: int):
    y = extractedNum
    y = y ^ (y << 18)



  def extract_number(self):
    if self.index >= self.n:
      if self.index > self.n:
        raise Exception("Generator was never seeded")
      self.twist()

    y = self.MT[self.index]
    y = y ^ ((y >> 11) & 0xFFFFFFFF)
    y = y ^ ((y << 7) & 0x9D2C5680)
    y = y ^ ((y << 15) & 0xEFC60000)
    y = y ^ (y >> 18)
    self.index += 1
    return y & 0xFFFFFFFF
    
  
def oracle():
  print("oracle sleeping for 5-60 seconds")
  sleep(random.randint(5, 60))
  oracleTime = int(time())
  mt = MersenneTwist(oracleTime)
  print("oracle time: {}".format(oracleTime))
  print("oracle sleeping for 5-60 seconds")
  sleep(random.randint(5, 60))
  return base64.b64encode(bytes(mt.extract_number()))

def bruteForceOracle():
  oracleNum = oracle()
  currTime = int(time())
  print("brute force time: {}".format(currTime))
  for i in range(currTime - 120, currTime):
    mt = MersenneTwist(i)
    if base64.b64encode(bytes(mt.extract_number())) == oracleNum:
      return i
  return None

def getToken(): 
  url = 'http://localhost:8080/forgot'
  baseTokens = []
  tokens = []

  mt = MersenneTwist(1)

  # for _ in range(78):
  #   x = requests.post(url, {"user": "daniel"})
  #   baseTokens.append(base64.b64decode(x.text.split("reset?token=")[1].split("<!--close_token-->")[0]).decode('utf-8')) 

  # # take each base token which is 8 tokens seperated by : and split them into 8 seperate tokens
  # # then add them to the tokens list  
  # for baseToken in baseTokens: 
  #   for token in baseToken.split(":"):
  #     tokens.append(int(token))

  for _ in range(624):
    tokens.append(mt.extract_number())

  # print("tokens: {}".format(tokens))
  # print("len tokens: {}".format(len(tokens)))

  mixedTokens = mix(tokens)

  # print("mixed tokens: {}".format(mixedTokens))
  # print("len mixed tokens: {}".format(len(mixedTokens)))

  predictedTokens = extractNumbers(mixedTokens)

  # print("predicted tokens: {}".format(predictedTokens))
  # print("len predicted tokens: {}".format(len(predictedTokens)))

  newBaseTokens = []
  newTokens = []

  # for _ in range(78):
  #   x = requests.post(url, {"user": "daniel"})
  #   newBaseTokens.append(base64.b64decode(x.text.split("reset?token=")[1].split("<!--close_token-->")[0]).decode('utf-8')) 

  # # take each base token which is 8 tokens seperated by : and split them into 8 seperate tokens
  # # then add them to the tokens list  
  # for baseToken in newBaseTokens: 
  #   for token in baseToken.split(":"):
  #     newTokens.append(int(token))

  for _ in range(624):
    newTokens.append(mt.extract_number())
  
  # print("new tokens: {}".format(newTokens))
  # print("len new tokens: {}".format(len(newTokens)))

  for i in range(len(newTokens)):
    print("=====================================")  
    print("new token: {}".format(newTokens[i]))
    print("predicted token: {}".format(predictedTokens[i]))
    if (newTokens[i] == predictedTokens[i]):
      print("token is the same")
    print("=====================================")


def mix(nums: list = None):
  n = 624
  r = 31
  m = 397
  a = 0x9908B0DF
  lower_mask = (1 << r) - 1
  upper_mask = (~lower_mask) & 0xFFFFFFFF

  for i in range(n):
    x = (nums[i] & upper_mask) + (nums[(i + 1) % n] & lower_mask)
    xA = x >> 1
    if x % 2 != 0:
      xA = xA ^ a
    nums[i] = nums[(i + m) % n] ^ xA

  return nums

def extractNumbers(nums: list = None):
  n = 624
  u = 11
  d = 0xFFFFFFFF
  s = 7
  b = 0x9D2C5680
  t = 15
  c = 0xEFC60000
  l = 18

  extractNums = []

  for i in range(n):
    y = nums[i]
    y = y ^ ((y >> u) & d)
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    y = y ^ (y >> l)
    extractNums.append(y & 0xFFFFFFFF)
  
  return extractNums

def main():
  # mt = MersenneTwist(0)
  # for _ in range(10):
  #   print(mt.extract_number())

  # print(bruteForceOracle())

  # getToken()

  # def extract_number(self):
  #   if self.index >= self.n:
  #     if self.index > self.n:
  #       raise Exception("Generator was never seeded")
  #     self.twist()

  #   y = self.MT[self.index]
  #   y = y ^ ((y >> 11) & 0xFFFFFFFF)
  #   y = y ^ ((y << 7) & 0x9D2C5680)
  #   y = y ^ ((y << 15) & 0xEFC60000)
  #   y = y ^ (y >> 18)
  #   self.index += 1
  #   return y & 0xFFFFFFFF
  
main()
