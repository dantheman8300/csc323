import base64
from random import randbytes
from Crypto.Cipher import AES

import requests

def encrypt_ecb(fileIn: str, fileOut: str, key=b'1234567812345678', bmp = False):
  # Read input file
  fileIn = open(fileIn, "rb")
  if (bmp):
    headerBytes = fileIn.read(54) # store header info

  # Create output file
  fileOut = open(fileOut, 'wb')
  if (bmp):
    fileOut.write(headerBytes)

  # Read first block of data
  block = fileIn.read(16)
  padded = False

  while(len(block) > 0):
    # create aes cipher
    cipher = AES.new(key, AES.MODE_ECB)

    if(len(block) < 16):
      block = padd(block)
      padded = True

    blockCipherText = cipher.encrypt(block)
    fileOut.write(blockCipherText)

    block = fileIn.read(16)

  # add full padded block if needed
  if (not padded):
    block = padd(b'')
    cipher = AES.new(key, AES.MODE_ECB)
    blockCipherText = cipher.encrypt(block)
    fileOut.write(blockCipherText)

def decrypt_ecb(fileIn: str, fileOut: str, key=b'1234567812345678', bmp = False):
  # Read input file
  fileIn = open(fileIn, "rb")
  # Create output file
  fileOut = open(fileOut, 'wb')

  if (bmp):
    headerBytes = fileIn.read(54) # store header info
  if (bmp):
    fileOut.write(headerBytes)

  # --- Decrypt ---
  block = fileIn.read(16)

  while(len(block) > 0):
    # create aes cipher
    cipher = AES.new(key, AES.MODE_ECB)
    # print(len(block))

    blockCipherText = cipher.decrypt(block)

    block = fileIn.read(16)
    

    if (len(block) == 0):
      blockCipherText = unpadd(blockCipherText)
      fileOut.write(blockCipherText)
    else:
      fileOut.write(blockCipherText)

def encrypt_cbc() -> bytes:
  # Read input file
  fileIn = open("mustang.bmp", "rb")
  headerBytes = fileIn.read(54) # store header info

  # Create output file
  fileOut = open("mustang-e-cbc.bmp", 'wb')
  fileOut.write(headerBytes)

  # Read first block of data
  block = fileIn.read(16)

  # gernerate IV
  prevCipherText = randbytes(16)
  iv = prevCipherText

  while(len(block) > 0):
    # create aes cipher
    key = b'1234567812345678'
    cipher = AES.new(key, AES.MODE_ECB)

    if(len(block) < 16):
      block = padd(block)

    blockCipherText = cipher.encrypt(xor(block, prevCipherText))
    fileOut.write(blockCipherText)

    prevCipherText = blockCipherText
    block = fileIn.read(16)

  return iv

# user=USERNAaaaaa
# user------------
# admin***********
# user************
# **&uid=UID&role=
# user------------

registerURL = 'http://localhost:8080/register'
loginURL = 'http://localhost:8080/'
homeURL = 'http://localhost:8080/home'
x = requests.post(registerURL, {"user": "USERNAaaaaa"+"user\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0A" + "", "password": "f"})
print(x.text)

x = requests.post(loginURL, {"user": "USERNAaaaaa"+"user\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0A" + "", "password": "f"})
print(x.text)
print(x.cookies)

# initialize a session
session = requests.Session()
  
# send a get request to the server
response = session.get(loginURL)
  
# print the response dictionary
print(session.cookies.get_dict())

# Take a file with hex encoded BMPs, seperated by a new line, and decode them
# into a file with the decoded BMPs
def parseBMPsFromFile(fileIn: str, fileOut: str):
  fileIn = open(fileIn, "r")
  # fileOut = open(fileOut, "w")

  encodedBMPs = fileIn.read().split("\n")

  for i in range(len(encodedBMPs)):
    encodedBMP = encodedBMPs[i]
    # print("Decoding BMP {}".format(i))
    if (len(encodedBMP) > 0):
      print("Decoding BMP {}".format(i))
      fileName = "bmps/" + fileOut + str(i) + ".bmp"
      outputFile = open(fileName, "wb")
      outputFile.write(bytes.fromhex(encodedBMP))


def padd(block: bytes):
  lengthOfBlock = len(block)
  paddingByte = (16 - lengthOfBlock).to_bytes(1, 'big')
  # print("padding byte: {}".format(paddingByte))

  while (lengthOfBlock < 16):
    block += paddingByte
    lengthOfBlock = len(block)

  return block

def unpadd(block: bytes):
  paddingByte = block[-1]
  print("padding byte: {}".format(paddingByte))

  blockArray = bytearray(block)

  for _ in range(paddingByte):
    if (blockArray[-1] != paddingByte):
      raise Exception("Invalid padding")
    blockArray.pop()

  return bytes(blockArray)

def base64DecodeFile(fileIn: str, fileOut: str):
  fileIn = open(fileIn, "r")
  fileOut = open(fileOut, "wb")

  fileOut.write(base64.b64decode(fileIn.read()))

# block = b''
# for _ in range(16):
#   print(block)
#   print(padd(block))
#   print(len(padd(block)))
#   print(unpadd(padd(block)))
#   block += b'1'

# base64DecodeFile("Lab2.TaskII.A.txt", "Lab2.TaskII.A.decoded.txt")
# decrypt_ecb("Lab2.TaskII.A.decoded.txt", "Lab2.TaskII.A.decrypted.txt", key = b'CALIFORNIA LOVE!')

# parseBMPsFromFile("Lab2.TaskII.B.txt", "decodedBMP")