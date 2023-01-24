from base64 import b64encode, b64decode

STANDARD_FREQUENCIES = {
  'e': 0.12702,
  't': 0.09056,
  'a': 0.08167,
  'o': 0.07507,
  'i': 0.06966,
  'n': 0.06749,
  's': 0.06327,
  'h': 0.06094,
  'r': 0.05987,
  'd': 0.04253,
  'l': 0.04025,
  'c': 0.02782,
  'u': 0.02758,
  'm': 0.02406,
  'w': 0.02360,
  'f': 0.02228,
  'g': 0.02015,
  'y': 0.01974,
  'p': 0.01929,
  'b': 0.01492,
  'v': 0.00978,
  'k': 0.00772,
  'j': 0.00153,
  'x': 0.00150,
  'q': 0.00095,
  'z': 0.00074
}



def xor (plain: str, key: str) -> str: 

  xorResHex = ""

  for i in range (0, len(plain)):
    plainChar = plain[i]
    keyChar = key[i % len(key)]
    xorCharInHex = str(hex(ord(plainChar) ^ ord(keyChar))).split('0x')[1].zfill(2)

    # print("plainChar : {}".format(plainChar))
    # print("keyChar : {}".format(keyChar))
    # print("xorCharInHex : {}".format(xorCharInHex))
    xorResHex += xorCharInHex

  # xorResString = hexToString(xorResHex)

  return xorResHex

def compareCharacterFrequencies (freq1: dict, freq2: dict) -> float:
  total = 0

  for key in freq1:
    if key in freq2:
      total += abs(freq1[key] - freq2[key])
    else:
      total += freq1[key]

  for key in freq2:
    if key not in freq1:
      total += freq2[key]

  return total

# Calculates the frequency of each character in a string
# the string is hex encoded
def calculateCharacterFrequency (string: str) -> dict:
  characterFrequency = {}

  for i in range(0, len(string), 2):
    charVal = int(string[i:i+2], 16)

    # ignore non letters
    if (charVal < 65 or (charVal > 90 and charVal < 97) or charVal > 122):
      continue

    # Make everything letter lowercase
    if (charVal >= 65 and charVal <= 90):
      charVal += 32

    char = chr(charVal)

    if char in characterFrequency:
      characterFrequency[char] += 1
    else:
      characterFrequency[char] = 1

  for key in characterFrequency:
    characterFrequency[key] = characterFrequency[key] / (len(string) * 2)

  return characterFrequency

def getAllXorResults (string: str) -> list:
  xorResults = []

  for i in range(0, 256):
    xorResults.append(xor(hexToString(string), chr(i)))

  return xorResults


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
print("hexToString: {} -> {}".format('61DD', hexToString('61DD')))
print("base64ToHex: {} -> {}".format('YWE=', base64ToHex('YWE=')))
print("hexToBase64: {} -> {}".format('6161', hexToBase64('6161')))

print("=========================================")

print(xor('cat', 'a'))

print("=========================================")

btxt = open('Lab0.TaskII.B.txt', 'r').read().split('\n')
btxt.pop()

amount = 1000

allXorResults = []
highestScore = {'score': -1, 'line': 0, 'xor': 0}

for cipher in btxt[:amount]:
  allXorResults.append(getAllXorResults(cipher))

for (i, cipher) in enumerate(btxt[:amount]):
  # print("Cipher {}:".format(i))
  cipherXorResults = allXorResults[i]
  for (j, result) in enumerate(cipherXorResults):
    charFreq = calculateCharacterFrequency(result)
    freqScore = compareCharacterFrequencies(charFreq, STANDARD_FREQUENCIES)
    # print("\tResult {}.{}:".format(i, j))
    # print("\t\tScore: {}".format(freqScore))
    if (freqScore < highestScore['score'] or highestScore['score'] == -1):
      highestScore = {'score': freqScore, 'line': i, 'xor': j}
      # print("\t\tHighest Score: {}".format(highestScore))
      # print("\t\tResult: {}".format(result))
      # print("\t\tCharacter Frequency: {}".format(charFreq))

print("=========================================")
print("highestScore: {}".format(highestScore))
print("Result: {}".format(hexToString(allXorResults[highestScore['line']][highestScore['xor']])))


# print(btxt[0])

# print(getAllXorResults(btxt[0]))

# for (i, result) in enumerate(getAllXorResults(btxt[0])):
#   print("Result {}:".format(i))
#   print(calculateCharacterFrequency(result))
#   print(compareCharacterFrequencies(calculateCharacterFrequency(result), STANDARD_FREQUENCIES))


# print("6161616161")

# print(getAllXorResults("6161616161"))

# for (i, result) in enumerate(getAllXorResults("6161616161")):
#   print("Result {}:".format(i))
#   print(calculateCharacterFrequency(result))
#   print(compareCharacterFrequencies(calculateCharacterFrequency(result), STANDARD_FREQUENCIES))


