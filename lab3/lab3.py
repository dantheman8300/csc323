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

    print("cipherTextBlocks: ", cipherTextBlocks)
    print("plainTextBlocks: ", plainTextBlocks)


    originalCipherChar = copy.copy(cipherTextBlocks[3][15])

    for charCode in range(256):  
        cipherTextBlocks[3][15] = originalCipherChar ^ charCode ^ ord('\x01')
        if (pad_oracle(assembleCipherText(cipherTextBlocks)) and cipherTextBlocks[3][15] != originalCipherChar):
            print('char1: "{}"'.format(chr(charCode)))
            plainTextBlocks[4][15] = charCode
            break

    originalCipherChar = copy.copy(cipherTextBlocks[3][14])
    # cipherTextBlocks[3][15] = originalCipherChar ^ ord('\n') ^ ord('\x02')

    for charCode in range(1, 256):  
        cipherTextBlocks[3][14] = originalCipherChar ^ charCode ^ ord('\x02')
        if (pad_oracle(assembleCipherText(cipherTextBlocks)) and cipherTextBlocks[3][14] != originalCipherChar):
            print('char2: {} -> "{}"'.format(charCode, chr(charCode)))
            plainTextBlocks[4][14] = charCode
            # break
  
    print("plainTextBlocks: ", plainTextBlocks)



def sha1(msg):
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    ml = int.to_bytes(len(msg), "big")
