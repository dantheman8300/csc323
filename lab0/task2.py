from base64 import b64encode, b64decode


def xor (plain: str, key: str) -> str: 
  # print("plain : {}".format(plain))
  # print("key : {}".format(key))
  # print("plain in ASCII : {}".format(ord(plain)))
  # print("plain in bits : {}".format(bin(ord(plain))))
  # print("key in ASCII : {}".format(ord(key)))
  # print("key in bits : {}".format(bin(ord(key))))
  # print("xor : {}".format(ord(plain) ^ ord(key)))

  xorResHex = ""

  for i in range (0, len(plain)):
    plainChar = plain[i]
    keyChar = key[i % len(key)]
    xorChar = str(ord(plainChar) ^ ord(keyChar)).zfill(2)

    print("plainChar : {}".format(plainChar))
    print("keyChar : {}".format(keyChar))
    print("xorChar : {}".format(xorChar))
    xorResHex += xorChar

  # xorResString = hexToString(xorResHex)

  return xorResHex


# Converts a ASCII encoded string to a hex encoded string
def stringToHex (string: str) -> str:
  return string.encode('utf-8').hex()

# Converts a hex encoded string to a ASCII encoded string
def hexToString (hex: str) -> str:

  asciiString = ""

  for i in range(0, len(hex), 2):
    asciiChar = chr(int(hex[i:i+2], 16))
    asciiString += asciiChar

  return asciiString

  

# Converts a base64 encoded string to a hex encoded string
def base64ToHex (base64: str) -> str:
  return b64decode(base64).hex()

# Converts a hex encoded string to a base64 encoded string
def hexToBase64 (hex: str) -> str:
  return b64encode(bytes.fromhex(hex)).decode('utf-8')

print("stringToHex: {} -> {}".format('aa', stringToHex('aa')))
print("hexToString: {} -> {}".format('6161', hexToString('6161')))
print("base64ToHex: {} -> {}".format('YWE=', base64ToHex('YWE=')))
print("hexToBase64: {} -> {}".format('6161', hexToBase64('6161')))

print("=========================================")

print(xor('cat', 'a'))

