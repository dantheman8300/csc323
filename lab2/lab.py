import base64
from random import randbytes
from Crypto.Cipher import AES

import requests

def encrypt_ecb(fileNameIn: str, fileNameOut: str, key=b'1234567812345678', bmp = False):
  # Read input file
  fileIn = open(fileNameIn, "rb")
  if (bmp):
    headerBytes = fileIn.read(54) # store header info

  # Create output file
  fileOut = open(fileNameOut, 'wb')
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

def decrypt_ecb(fileNameIn: str, fileNameOut: str, key=b'1234567812345678', bmp = False):
  # Read input file
  fileIn = open(fileNameIn, "rb")
  # Create output file
  fileOut = open(fileNameOut, 'wb')

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

def encrypt_cbc(fileNameIn: str, fileNameOut: str, key=b'1234567812345678',  bmp = False, iv = randbytes(16)) -> bytes:
  # Read input file
  fileIn = open(fileNameIn, "rb")
  if (bmp):
    headerBytes = fileIn.read(54) # store header info

  # Create output file
  fileOut = open(fileNameOut, 'wb')
  if (bmp):
    fileOut.write(headerBytes)

  # Read first block of data
  block = fileIn.read(16)
  padded = False

  # gernerate IV
  prevCipherText = iv

  while(len(block) > 0):
    # create aes cipher
    cipher = AES.new(key, AES.MODE_ECB)

    if(len(block) < 16):
      block = padd(block)
      padded = True

    blockCipherText = cipher.encrypt(xor(block, prevCipherText))
    fileOut.write(blockCipherText)

    prevCipherText = blockCipherText
    block = fileIn.read(16)

  # add full padded block if needed
  if (not padded):
    block = padd(b'')
    cipher = AES.new(key, AES.MODE_ECB)
    blockCipherText = cipher.encrypt(xor(block, prevCipherText))
    fileOut.write(blockCipherText)

  return iv

def decrypt_cbc(fileNameIn: str, fileNameOut: str, key, bmp = False) -> bytes:
  # Read input file
  fileIn = open(fileNameIn, "rb")
  if (bmp):
    headerBytes = fileIn.read(54) # store header info

  # Create output file
  fileOut = open(fileNameOut, 'wb')
  if (bmp):
    fileOut.write(headerBytes)

  # get IV
  iv = fileIn.read(16)
  prevCipherText = iv

  # Read first block of data
  block = fileIn.read(16)

  while(len(block) > 0):
    # create aes cipher
    cipher = AES.new(key, AES.MODE_ECB)

    blockCipherText = xor(cipher.decrypt(block), prevCipherText)
    fileOut.write(blockCipherText)

    prevCipherText = block
    block = fileIn.read(16)

    # if (len(block) == 0):
    #   blockCipherText = unpadd(blockCipherText)
    #   fileOut.write(blockCipherText)
    # else:
    #   fileOut.write(blockCipherText)

  return iv

def decrypt_cbc_actual(fileNameIn: str, fileNameOut: str, iv: bytes, key, bmp = False):
  # Read input file
  fileIn = open(fileNameIn, "rb")
  if (bmp):
    headerBytes = fileIn.read(54) # store header info

  # Create output file
  fileOut = open(fileNameOut, 'wb')
  if (bmp):
    fileOut.write(headerBytes)

  # Read first block of data
  block = fileIn.read()

  # Decrypt

  # create aes cipher

  cipher = AES.new(key, AES.MODE_CBC, iv)

  blockCipherText = cipher.decrypt(block)
  fileOut.write(blockCipherText)

# user=12345678912
# user------------
# admin-----------
# user------------
# 123&uid=12&role=
# user------------

def ECBCookies():
  session = requests.Session()
  url = 'http://localhost:8080/register'
  url2 = 'http://localhost:8080/'
  url3 = 'http://localhost:8080/home'
  username = "12345678912" + "user\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0C" + "admin\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0B" + "user\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0C" + "123"
  password = 'a'

  # register
  z = session.post(url, {"user" : username, "password" : password})

  # login
  y = session.post(url2, {"user" : username, "password" : password})

  # get cookie on home page
  x = session.get(url3)
  cookie = session.cookies['auth_token']

  # print cookie in blocks of 16 bytes
  print("OG Cookie: ")
  for i in range(0, len(cookie), 32):
    print(cookie[i:i+32])

  # attack cookie - replace the last 32 characters with the third 32 character block
  cookie = cookie[:160] + cookie[64:96]

  # print cookie in blocks of 16 bytes
  print("Attacked Cookie: ")
  for i in range(0, len(cookie), 32):
    print(cookie[i:i+32])

  print("cookie: {}".format(cookie))

# 1234567812345678
# user=123456789&u
# id=2&role=user--

def CBCCookies():
  session = requests.Session()
  url = 'http://localhost:8080/register'
  url2 = 'http://localhost:8080/'
  url3 = 'http://localhost:8080/home'
  username = '123456789'
  password = 'a'

  # register
  z = session.post(url, {"user" : username, "password" : password})

  # login
  y = session.post(url2, {"user" : username, "password" : password})

  # get cookie on home page
  x = session.get(url3)
  cookie = session.cookies['auth_token']

  # print cookie in blocks of 16 bytes
  print("OG Cookie: ")
  for i in range(0, len(cookie), 32):
    print(cookie[i:i+32])

  # attack cookie - perform bit flipping attack
  cookie = bytearray.fromhex(cookie)
  cookie[10 + 16] = cookie[10 + 16] ^ ord('u') ^ ord('a')
  cookie[11 + 16] = cookie[11 + 16] ^ ord('s') ^ ord('d')
  cookie[12 + 16] = cookie[12 + 16] ^ ord('e') ^ ord('m')
  cookie[13 + 16] = cookie[13 + 16] ^ ord('r') ^ ord('i')
  cookie[14 + 16] = cookie[14 + 16] ^ ord('\x00') ^ ord('n')
  cookie[15 + 16] = cookie[15 + 16] ^ ord('\x02') ^ ord('\x01')

  cookie = cookie.hex()

  # print attacked cookie in blocks of 16 bytes
  print("Attacked Cookie: ")
  for i in range(0, len(cookie), 32):
    print(cookie[i:i+32])

  print('cookie: {}'.format(cookie))


  # # print cookie in blocks of 16 bytes
  # print("Attacked Cookie: ")
  # for i in range(0, len(cookie), 32):
  #   print(cookie[i:i+32])

  # print("cookie: {}".format(cookie))

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

def xor(a: bytes, b: bytes) -> bytes:
  xorBytes = b''

  for i in range(len(a)):
    xorBit = a[i]^b[i]
    xorBitByte = xorBit.to_bytes(1, 'big')
    xorBytes += xorBitByte

  return xorBytes  

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

# ECBCookies()  

# CBCCookies()

base64DecodeFile("Lab2.TaskIII.A.txt", "Lab2.TaskIII.A.decoded.txt")
# # decrypt_cbc_actual("Lab2.TaskIII.A.decoded.txt", "Lab2.TaskIII.A.decrypted.actual.txt", key = b'MIND ON MY MONEY', iv=b'MONEY ON MY MIND')
decrypt_cbc("Lab2.TaskIII.A.decoded.txt", "Lab2.TaskIII.A.decrypted.txt", key = b'MIND ON MY MONEY')
# iv = encrypt_cbc("cp-logo.bmp", "cp-logo-cbc.bmp", key = b'CALIFORNIA LOVE!', bmp=True)
# decrypt_cbc("cp-logo-cbc.bmp", "cp-logo-cbc-decrypted.bmp", iv, key = b'CALIFORNIA LOVE!', bmp=True)
# decrypt_cbc_actual("cp-logo-cbc.bmp", "cp-logo-cbc-decrypted.bmp", iv)