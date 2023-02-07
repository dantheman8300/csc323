import base64 
import time
import random
import requests
# need general xor
# str to hex


# encode strings to hexadecimal
def str_2_hex(s) -> str:
    return s.encode(encoding='UTF-8', errors='strict').hex()

# decode hexadecimal to strings
def hex_2_str(h) -> str:
    result = ""
    for i in range(0, len(h) - 1, 2):
        result += chr(int(h[i:i+2], 16))
    return result

# decode base64 to hexadecimal
def base64_2_hex(b) -> str:
    return base64.b64decode(b).hex()

# encode hexadecimal to base64
def hex_2_base64(h) -> str:
    return base64.b64encode(bytes.fromhex(h)).decode()


# task 2 part A
## Implement XOR 
def xor(p, k):
    result = ""
    keyInd = 0

    # if key < plaintext -> repeat key
    if(len(k) < len(p)):
        for x in p:
            result += chr(x ^ k[keyInd % len(k)])
            keyInd += 1
    else:
        for x in p:
            result += chr(x ^ k[keyInd])
            keyInd += 1
    return str_2_hex(result)

# Task 1 - PRGs

## Implement the MT19937 Mersenne Twister
# period length = mersenne prime # = 2^p-1 (where p is some prime number)
# MT19937 = 2^19937-1 (32 bit word length)
# verify that it is deterministic
# w = word size = 32
# n = degree of recurrance = 624
# m = middle word = 397
# r = separation point = 31
# a = cofficients of rational normal = 0x9908B0DF
# b,c = TGFSR(R) termpering bitmasks = 0x9D2C5680, 0xEFC60000
# s,t = TGFSR(R) tempering bit shifts = 9, 15
# u,d,l = addtl MT tempering bit shifts/masks = 11, 0xFFFFFFFF, 18


class MerTwist:
    # store state of the generator
    def __init__(self, seed):
        (self.w, self.n, self.m, self.r) = (32, 624, 397, 31)
        (self.a, self.b, self.c) = (0x9908B0DF, 0x9D2C5680, 0xEFC60000)
        (self.s, self.t, self.u) = (7, 15, 11)
        (self.d, self.l, self.f) = (0xFFFFFFFF, 18, 1812433253)
        self.MT = [0] * self.n
        self.index = self.n + 1
        self.lower_mask = (1 << self.r) - 1 # the binary # of r 1's
        self.upper_mask = 0xFFFFFFFF & (~self.lower_mask) # lowest w bits of (not lower_mask)

        self.seed_mt(int(seed))


    # initialize generator from a seed
    def seed_mt(self, seed):
        self.index = self.n
        self.MT[0] = seed

        for i in range(1, self.n):
            self.MT[i] = (self.f * (self.MT[i-1] ^ (self.MT[i-1] >> (self.w-2))) + i) & 0xFFFFFFFF #lowest w bits of (f * (MT[i-1] xor (MT[i-1] >> (w-2))) + i)



    # Extract a tempered value based on MT[index]
    # calling twist() every n numbers
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



    # Generate the next n values from the series x_i 
    def twist(self):
        for i in range(self.n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i+1) % self.n] & self.lower_mask)
            xA = x >> 1
            if (( x % 2) != 0):
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
        self.index = 0



## Break it 
# oracle - can answer questions
def oracle():
    # wait bet 5 and 60 secs chosen randomly
    time.sleep(random.randint(5,60))

    # seeds MT 19937 using current UNIX timestamp
    mt = MerTwist(int(time.time()))

    # wait another randomly chosen number of seconds between 5 and 60
    time.sleep(random.randint(5,60))

    # return the first 32 bit output as a base64 encoded value
    # return base64.b64encode(bytes(mt.extract_number()))
    return mt.extract_number()

def breakMT():
    num = oracle()
    t = int(time.time())
    guessed = False
    for i in range(int(time.time()) - 120, t):
        mt = MerTwist(i)
        num2 = mt.extract_number()
        if(num2 == num):
            print("YAAY ", num2, " ", num)
            guessed = True

    if(guessed == False):
       print("sad")


def unmix(token):
    # request 78 consecutive password reset tokens from eortiz
    # recreate initial state of generator and predict all future password resets
    token = base64.b64decode(token).decode('utf-8')
    print(token)
    t = token.split(":")
    t.remove("")
    print(t)
    for i in range(len(t)):
        t[i] = int(t[i])
    return t


def main():
    # mt = MerTwist(0)

    # for i in range(10):
    #     print(mt.extract_number())

    # print(oracle())

    # breakMT()
    url = 'http://localhost:8080/forgot'
    b64tokens = []

    for i in range(78):
        x = requests.post(url, {"user": "emelia"})
        b64tokens.append(x.text.split("reset?token=")[1].split("<!--close_token-->")[0])

    print(b64tokens)

main()










