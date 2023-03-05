from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import requests
import copy

# This function is used to determine the character at the given index of the 
# given cipherblock's plaintext. It does this by padding the cipherblock up to 
# the given index with all possible characters until the padding is valid. We 
# will use a padding oracle to make this determination.  
def padAttackOneChar(cipherblock: bytearray, index: int, previousChars: bytearray):
  cipherCharAtIndex = cipherblock[index]
  currChar = 0

  # initialize the padding of all previous characters
  paddingByte = (16 -( index + 1)).to_bytes(1, byteorder='big')
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
    if (pad_oracle(cipherblock)):
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




def pad_oracle(cipherText: bytearray):

    url= 'http://localhost:8080/'


    # check for 404 (not found) or 403 (forbidden)
    check = requests.get(url, {"enc": cipherText}).text
    if ("403" in check):
      return False
    if ("404" in check):
      return True

def main():
  cipherTextHex = getCipherText()
  # print cipherTextHex in blocks of 32 characters
  for i in range(0, len(cipherTextHex), 32):
    print(cipherTextHex[i:i+32])
    

  cipherText = bytearray.fromhex(cipherTextHex)


  originalCipherChar = copy.copy(cipherText[15 + 16 * 2])

  for i in range(256): 
    cipherText[15 + 16 * 2] = originalCipherChar ^ i ^ ord('\01')
    attackedCipherTextHex = cipherText.hex()
    if (pad_oracle(cipherText)):
      print('char: ', i)
      print("attackedCipherTextHex: ", attackedCipherTextHex)
      break

  print('end')

  







main()
