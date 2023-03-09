import struct
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import requests
import copy

  
def getCipherText(): 
    url = 'http://localhost:8080/eavesdrop'

    # get leaked cipher text
    req = requests.get(url).text
    cipher = req.split("<font color=\"red\"> ")[1].split(" </font></p>")[0]
    return cipher

def disassembleCipherText(cipherTextHex: str):
    cipherText = bytearray.fromhex(cipherTextHex)
    cipherBlocks = []
    for i in range(0, len(cipherText), 16):
        cipherBlocks.append(cipherText[i:i+16])
    return cipherBlocks

def assembleCipherText(cipherBlocks: list):
    cipherText = bytearray()
    for block in cipherBlocks:
        cipherText += block
    return cipherText.hex()


def pad_oracle(cipherText: bytearray):
    url= 'http://localhost:8080/'

    # check for 404 (not found) or 403 (forbidden)
    check = requests.get(url, {"enc": cipherText}).text
    if ("403" in check):
        return False
    if ("404" in check):
        return True

def task_1():
    cipherTextHex = getCipherText()
    cipherTextBlocks = disassembleCipherText(cipherTextHex)
  
    plainTextBlocks = [bytearray(16) for i in range(len(cipherTextBlocks))]
    templateBlock = bytearray(16)

    for blockIndex in range(1, len(cipherTextBlocks)):
        for i in range(15, -1, -1):
            paddingByte = (16 - ( i )).to_bytes(1, byteorder='big')
            for j in range(i + 1, 16):
                templateBlock[j] = cipherTextBlocks[blockIndex - 1][j] ^ plainTextBlocks[blockIndex][j] ^ ord(paddingByte)
            for charCode in range(0, 256):  
                templateBlock[i] = cipherTextBlocks[blockIndex - 1][i] ^ charCode ^ ord(paddingByte)
                if (pad_oracle(templateBlock + cipherTextBlocks[blockIndex])):
                # print('char: i: {} blockIndex: {} "{}"'.format(i, blockIndex, chr(charCode)))
                    plainTextBlocks[blockIndex][i] = charCode
                    break



  # print("cipherTextBlocks: ", cipherTextBlocks)
    print("plainTextBlocks: ", (plainTextBlocks[1] + plainTextBlocks[2]))


# Task II
def sha1(msg):
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    message = bytearray(msg, 'utf-8')
    ml = 8 * len(message)
    message.append(0x80)
    while len(message) % 64 != 56:
        message.append(0x00)
    message += struct.pack(">Q", ml)

 # Process message in 512-bit chunks
    for i in range(0, len(message), 64):
        chunk = message[i:i+64]

        # Break chunk into 16 32-bit words
        w = list(struct.unpack(">16L", chunk))

        # Extend the 16 32-bit words into 80 32-bit words
        for j in range(16, 80):
            w.append((((w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16]) << 1) | ((w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16]) >> 31)) & 0xFFFFFFFF)

        # Initialize hash value for this chunk
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        # Main loop
        for j in range(80):
            if j <= 19:
                f = (b & c) ^ ((~b) & d)
                k = 0x5A827999
            elif j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif j <= 59:
                f = (b & c) ^ (b & d) ^ (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (((a << 5) | (a >> 27)) & 0xFFFFFFFF) + f + e + k + w[j] & 0xFFFFFFFF
            e = d
            d = c
            c = (((b << 30) | (b >> 2)) & 0xFFFFFFFF)
            b = a
            a = temp

        # Add this chunk's hash to result so far
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    # Produce the final hash value
    return "%08x%08x%08x%08x%08x" % (h0, h1, h2, h3, h4)
    # return (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4


def test_sha(msg, ans):
    hash = sha(msg, 50) 
    hash2 = sha(ans, 50) 
    # if(hash == sha1(ans)):
    print("sha hash: " + hash)
    print("sha hash: " + hash2)
    print("string 1: " + msg)
    print("string 2: " + ans)
    print("correct!")
    # else:
    #     print(msg)
    #     print(ans)
    #     print("sad:(")


def sha(inputText: str, bits: int): 
  key = sha1(inputText)
  key = int(key, 16)
  key = '{:b}'.format(key)
  return key[0:bits]

# test_sha('"4QA', "HS&[")

def findCollisionBirthday(bits: int):
  hashes = {}
  currentMessage = ' '
  currentHash = ''
  currentIndexToIncrement = 0
  numInputs = 0
  startTime = time.time()

  while(True):
    numInputs += 1

    currentMessageBytes = bytearray(currentMessage, 'utf-8')
    while(currentMessageBytes[currentIndexToIncrement] >= 126):
      if (currentIndexToIncrement == 0):
        currentMessage = ' '*(len(currentMessage)+1)
        currentMessageBytes = bytearray(currentMessage, 'utf-8')
        currentIndexToIncrement = len(currentMessageBytes) - 1
        break
      currentMessageBytes[currentIndexToIncrement] = 32 # space
      currentMessageBytes[currentIndexToIncrement - 1] += 1
      currentIndexToIncrement -= 1
    currentIndexToIncrement = len(currentMessageBytes) - 1
    
    currentMessageBytes[currentIndexToIncrement] += 1
    currentMessage = currentMessageBytes.decode()
    currentHash = sha(currentMessage, bits)

    existingMessage = hashes.get(currentHash)

    if(existingMessage != None):
      endTime = time()

      totalElapsedTime = endTime - startTime

      collisionOutputFile = open('collision-{}.txt'.format(bits), 'w')

      collisionOutputFile.write('collision message 1: \"{}\"\n'.format(currentMessage))
      collisionOutputFile.write('collision message 2: \"{}\"\n'.format(existingMessage))
      collisionOutputFile.write('elapsed time: {:.6f} seconds\n'.format(totalElapsedTime))
      collisionOutputFile.write('inputs tested: {}\n'.format(numInputs))

      collisionOutputFile.close()
      
      return(bits, existingMessage, currentMessage, totalElapsedTime, numInputs)

    hashes[currentHash] = currentMessage


# print(findCollisionBirthday(50))

def findAllCollisionsBirthday():
  for i in range(8, 51, 2):
    print(findCollisionBirthday(i))



# Task III 
def len_ext_attack():
    return 0

def hmac_sha1():
    return 0



# Task IV

def time_attack():
    return 0

def improve_attack():
    return 0

def const_time_verify():
    return 0







# test_sha(sha1(""), "da39a3ee5e6b4b0d3255bfef95601890afd80709")
# test_sha(sha1("abc"), "a9993e364706816aba3e25717850c26c9cd0d89d")
# test_sha(sha1("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"), "84983e441c3bd26ebaae4aa1f95129e5e54670f1")
# test_sha(sha1("abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu"), "a49b2446a02c645bf419f995b67091253a04a259")

# task_1()

# findAllCollisionsBirthday()