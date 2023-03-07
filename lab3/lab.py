from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import requests
import copy
# from tqdm import tqdm

# This function is used to determine the character at the given index of the 
# given cipherblock's plaintext. It does this by padding the cipherblock up to 
# the given index with all possible characters until the padding is valid. We 
# will use a padding oracle to make this determination.  
def padAttackOneChar(cipherblock: bytearray, index: int, previousChars: bytearray):
  cipherCharAtIndex = cipherblock[index]
  currChar = 0

  # initialize the padding of all previous characters
  paddingByte = (16 - ( index + 1)).to_bytes(1, byteorder='big')
  print("paddingByte: ", paddingByte)
  i = index + 1
  for char in previousChars:
    cipherblock[i] ^= char ^ ord(paddingByte)
    i += 1
  
  # cipher = AES.new(b'YELLOW SUBMARINE', AES.MODE_ECB)
  # cipherBlock = cipher.decrypt(cipherblock)
  # print("cipherBlock: ", cipherBlock)

  # pad the cipherblock with all possible characters until the padding is valid
  while (currChar < 256):
    cipherblock[index] = cipherCharAtIndex ^ currChar ^ ord(paddingByte)
    if (pad_oracle(cipherblock) and currChar != 1):
      print("currChar: ", currChar)
      print("cipherblock: ", cipherblock)
      return currChar
    currChar += 1

  # raise Exception("No valid padding found")


  
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
    print(block)
    cipherText += block
  
  return cipherText.hex()


def pad_oracle(cipherText: bytearray):

    url= 'http://localhost:8080/'


    # check for 404 (not found) or 403 (forbidden)
    check = requests.get(url, {"enc": cipherText.hex()}).text
    if ("403" in check):
      return False
    if ("404" in check):
      return True
    
def submitMessage(message: str):
  url = 'http://localhost:8080/submit'
  req = requests.post(url, {"guess": message}).text.split("<font color=\"black\">")[1].split("</font></p>")[0]

  print(req)

def main():
  cipherTextHex = getCipherText()
  # print cipherTextHex in blocks of 32 characters
  # for i in range(0, len(cipherTextHex), 32):
  #   print(cipherTextHex[i:i+32])

  # print("initial pad_oracle: ", pad_oracle(cipherTextHex))
    
  cipherTextBlocks = disassembleCipherText(cipherTextHex)
  # for (i, block) in enumerate(cipherTextBlocks):
  #   print("block {}: {}".format(i, block))
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

  # submitMessage("So I roll through good")


  # originalCipherChar = copy.copy(cipherTextBlocks[3][15])

  # for charCode in range(256):  
  #   cipherTextBlocks[3][15] = originalCipherChar ^ charCode ^ ord('\x01')
  #   if (pad_oracle(assembleCipherText(cipherTextBlocks)) and cipherTextBlocks[3][15] != originalCipherChar):
  #     print('char1: "{}"'.format(chr(charCode)))
  #     plainTextBlocks[4][15] = charCode
  #     break
  # cipherTextBlocks[3][15] = originalCipherChar



  # originalCipherChar = copy.copy(cipherTextBlocks[3][14])
  # # cipherTextBlocks[3][15] = originalCipherChar ^ ord('\n') ^ ord('\x02')

  # for charCode in range(1, 256):  
  #   cipherTextBlocks[3][14] = originalCipherChar ^ charCode ^ ord('\x02')
  #   if (pad_oracle(assembleCipherText(cipherTextBlocks)) and cipherTextBlocks[3][14] != originalCipherChar):
  #     print('char2: {} -> "{}"'.format(charCode, chr(charCode)))
  #     plainTextBlocks[4][14] = charCode
  #     # break
  
  # print("plainTextBlocks: ", plainTextBlocks)

  # print('end')

  







main()
