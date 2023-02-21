import base64
import random
from time import sleep, time
import requests

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

  # re-shift/xor/mask (like in extract_number)
  def mix(self, y):
    y = y ^ ((y >> self.u) & self.d)
    y = y ^ ((y << self.s) & self.b)
    y = y ^ ((y << self.t) & self.c)
    y = y ^ (y >> self.l)
    return y & 0xFFFFFFFF

  def twist(self):
    for i in range(self.n):
      x = (self.MT[i] & self.upper_mask) + (self.MT[(i + 1) % self.n] & self.lower_mask)
      xA = x >> 1
      if x % 2 != 0:
        xA = xA ^ self.a
      self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
    self.index = 0

  # re-twist our mt array 
  def ourTwist(self, foundMT):
    for i in range(self.n):
      x = (foundMT[i] & self.upper_mask) + (foundMT[(i + 1) % self.n] & self.lower_mask)
      xA = x >> 1
      if x % 2 != 0:
        xA = xA ^ self.a
      foundMT[i] = foundMT[(i + self.m) % self.n] ^ xA
    return foundMT

  # xor and right shift to undo extract # right shift
  def undoRightShift(self, val, shift):
    result = val
    for _ in range(32):
      result = val ^ (result >> shift)
    return result

  # xor, left shift and mask to undo extract # left shift  
  def undoLeftShift(self, val, shift, mask):
    result = val
    for _ in range(32):
      result = val ^ (result << shift & mask)
    return result

  # unmix extract_number to get to original state
  def unmix2(self, token):
    token = self.undoRightShift(token, self.l)
    token = self.undoLeftShift(token, self.t, self.c)
    token = self.undoLeftShift(token, self.s, self.b)
    token = self.undoRightShift(token, self.u)

    return token
    

# task # 1
def oracle():
  print("oracle sleeping for 5-60 seconds")
  sleep(random.randint(5, 60))
  oracleTime = int(time())
  mt = MersenneTwist(oracleTime)
  print("oracle time: {}".format(oracleTime))
  print("oracle sleeping for 5-60 seconds")
  sleep(random.randint(5, 60))
  return base64.b64encode(bytes(mt.extract_number()))

# break MT
def bruteForceOracle():
  oracleNum = oracle()
  currTime = int(time())
  print("brute force time: {}".format(currTime))
  for i in range(currTime - 120, currTime):
    mt = MersenneTwist(i)
    if base64.b64encode(bytes(mt.extract_number())) == oracleNum:
      return i
  return None

# Task # 2 
def getToken(): 
  forgetURL = 'http://localhost:8080/forgot'
  registerURL = 'http://localhost:8080/register'
  baseTokens = []
  tokens = []

  mt = MersenneTwist(1)

  requests.post(registerURL, {"user": "daniel", "password": "password"})

  # generate 78 user tokens
  for _ in range(78):
    x = requests.post(forgetURL, {"user": "daniel"})
    baseTokens.append(base64.b64decode(x.text.split("reset?token=")[1].split("<!--close_token-->")[0]).decode('utf-8')) 

  # # take each base token which is 8 tokens seperated by : and split them into 8 seperate tokens
  # # then add them to the tokens list  
  for baseToken in baseTokens: 
    for token in baseToken.split(":"):
      tokens.append(int(token))

  internalTokens = []

  for i in range(624):
    internalTokens.append(mt.unmix2(tokens[i]))

  ourTwisted = mt.ourTwist(internalTokens)

  resetToken = str(mt.mix(ourTwisted[0]))

  for i in range(1, 8):
    resetToken += ":" + str(mt.mix(ourTwisted[i]))

  x = requests.post(forgetURL, {"user": "admin"})

  resetToken = base64.b64encode(resetToken.encode('utf-8')).decode('utf-8')
  # print("reset link: http://localhost:8080/reset?token={}".format(resetToken))

  password = input("Enter admin's new password: ")

  x = requests.post("http://localhost:8080/reset?token={}".format(resetToken), {"password": password})

def main():
  # task 1
  # mt = MersenneTwist(0)
  # for _ in range(10):
  #   print(mt.extract_number())

  # print(bruteForceOracle())

  # task 2
  getToken()
  
main()
