from base64 import b64encode, b64decode
from time import time
import math 

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

def singleByteXor ():
  startTime = time()
  btxt = open('Lab0.TaskII.B.txt', 'r').read().split('\n')
  btxt.pop()

  amount = 1000

  allXorResults = []
  highestScore = {'score': -1, 'line': 0, 'xor': 0}

  for i in range(0, amount):
    cipher = btxt[i]
    # allXorResults.append(getAllXorResults(cipher))
    cipherXorResults = getAllXorResults(cipher)
    for j in range(0, len(cipherXorResults)):
      result = cipherXorResults[j]
      charFreq = calculateCharacterFrequency(result)
      freqScore = compareCharacterFrequencies(charFreq, STANDARD_FREQUENCIES)
      if (freqScore < highestScore['score'] or highestScore['score'] == -1):
        highestScore = {'score': freqScore, 'line': i + 1, 'xor': j}
        # print potential text
        print("score: {}".format(highestScore))
        print("\t\tPotential Text: {}".format(hexToString(result)))

  # for (i, cipher) in enumerate(btxt[:amount]):
  #   # print("Cipher {}:".format(i))
  #   cipherXorResults = allXorResults[i]
  #   for (j, result) in enumerate(cipherXorResults):
  #     charFreq = calculateCharacterFrequency(result)
  #     freqScore = compareCharacterFrequencies(charFreq, STANDARD_FREQUENCIES)
  #     # print("\tResult {}.{}:".format(i, j))
  #     # print("\t\tScore: {}".format(freqScore))
  #     if (freqScore < highestScore['score'] or highestScore['score'] == -1):
  #       highestScore = {'score': freqScore, 'line': i, 'xor': j}
  #       # print("\t\tHighest Score: {}".format(highestScore))
  #       # print("\t\tResult: {}".format(result))
  #       # print("\t\tCharacter Frequency: {}".format(charFreq))
  #       #print potential text
  #       print("\t\tPotential Text: {}".format(hexToString(result)))

  
  endTime = time()

  print("=========================================")
  print("Time taken: {}".format(endTime - startTime))
  print("highestScore: {}".format(highestScore))
  # print("Result: {}".format(hexToString(allXorResults[highestScore['line']][highestScore['xor']])))


def multiByteXor():
  startTime = time()
  intervalTime = time()
  ctxt = open('Lab0.TaskII.C.txt', 'r').read().split('\n')
  ctxt.pop()
  ctxt = ''.join(ctxt)
  ctxt = hexToString(base64ToHex(ctxt))

  keyA = 'abcdefghijklmnopqrstuvwxyz'

  biggestDifferencePercentage = 0
  biggestDifferenceKeyLength = 0

  # xorResHex = xor(ctxt, keyA)
  # # xorResString = hexToString(xorResHex)
  # freq = calculateCharacterFrequency(xorResHex)
  # print("freq: {}".format(freq))

  fileAverage = open("outputAverage.txt", "w")
  fileEach = open("outputEach.txt", "w")

  for i in range(1, len(keyA) + 1): # key length
    key = keyA[:i]
    strings = []
    for j in range(0, i):
      strings.append(ctxt[j::i])

    differencePercentageSum = 0

    for j in range(0, i):
      freq = calculateCharacterFrequency(xor(strings[j], key[j]), False)
      differencePercentageSum += (max(freq.values()) - min(freq.values())) / sum(freq.values()) * 100
      # print("freq: {}".format(freq))
      # print("+++++++++++++++++++++++++++++")
      # print("key length: {}".format(i))
      # print("largest frequency value: {}".format(max(freq.values())))
      # print("Smallest frequency value: {}".format(min(freq.values())))
      # print("biggest difference: {}".format(max(freq.values()) - min(freq.values())))
      # print("biggest difference percentage: {}".format((max(freq.values()) - min(freq.values())) / sum(freq.values()) * 100))
      # print("average freq: {}".format(sum(freq.values()) / len(freq)))
      # print("+++++++++++++++++++++++++++++")
      # file.write("+++++++++++++++++++++++++++++\n")
      # file.write("key length: {}\n".format(i))
      # file.write("largest frequency value: {}\n".format(max(freq.values())))
      # file.write("Smallest frequency value: {}\n".format(min(freq.values())))
      # file.write("biggest difference: {}\n".format(max(freq.values()) - min(freq.values())))
      fileEach.write("{}:\t{} {:.2f}\n".format(i, "=" * math.floor(((max(freq.values()) - min(freq.values())) / sum(freq.values()) * 100)), (max(freq.values()) - min(freq.values())) / sum(freq.values()) * 100))
      # file.write("average freq: {}\n".format(sum(freq.values()) / len(freq)))
      # file.write("+++++++++++++++++++++++++++++\n")

    averageDifferencePercentage = differencePercentageSum / i
    fileAverage.write("{}:\t{} {:.2f}\n".format(i, "=" * math.floor(averageDifferencePercentage), averageDifferencePercentage))

    if (averageDifferencePercentage > biggestDifferencePercentage):
      biggestDifferencePercentage = averageDifferencePercentage
      biggestDifferenceKeyLength = i


  print("biggestDifferencePercentage: {}".format(biggestDifferencePercentage))
  print("biggestDifferenceKeyLength: {}".format(biggestDifferenceKeyLength))

  fileAverage.close()
  fileEach.close()

  numbers = []
  numbers.extend(range(0, 256))
  possibleKeyVals = []
  for i in range(0, biggestDifferenceKeyLength):
    possibleKeyVals.append(numbers.copy())
  # print("possibleKeyVals: {}".format(possibleKeyVals))

  for j in range(0, len(ctxt)):
    print("char: {}".format(ctxt[j]))
    print("j: {}".format(j))
    i = 0
    while(i < len(possibleKeyVals[j % biggestDifferenceKeyLength])):
      # print("i: {}".format(i))
      # print("possibleKeyVals[j][i]: {}".format(possibleKeyVals[j][i]))
      xorRes = int(xor(ctxt[j], chr(possibleKeyVals[j % biggestDifferenceKeyLength][i])), 16)
      # print("xorRes: {}".format(xorRes))
      if (xorRes < 0 or xorRes > 126):
        print("removing: {}".format(possibleKeyVals[j % biggestDifferenceKeyLength][i]))
        possibleKeyVals[j % biggestDifferenceKeyLength].pop(i)
        i -= 1
      i += 1

  print("possibleKeyVals: {}".format(possibleKeyVals))

  key = [0] * biggestDifferenceKeyLength
  currIndex = 0

  bestScore = {'score': -1, 'key': [], 'plaintext': ""}

  
  while (currIndex < biggestDifferenceKeyLength): 
    for i in range(0, biggestDifferenceKeyLength):
      if (key[i] not in possibleKeyVals[i]):
        continue
    # print("key: {}".format(key))
    xorKey = ''.join([chr(x) for x in key])
    # print("xorKey: {}".format(xorKey))
    xorResHex = xor(ctxt, xorKey)
    score = compareCharacterFrequencies(calculateCharacterFrequency(xorResHex), STANDARD_FREQUENCIES)
    xorResString = hexToString(xorResHex)
    # print("score: {}".format(score))
    # print alive text every 5 minutes
    if (time() - intervalTime > 60):
      intervalTime = time()
      print("==================================================================================")
      print("Still ticking...")
      print("elapsed time: {}".format((time() - startTime) / 60))
      print("key: {}".format(key))
      print("==================================================================================")
    if (score < bestScore['score'] or bestScore['score'] == -1):
      bestScore = {'score': score, 'key': key.copy(), 'plaintext': xorResString}
      # print("bestScore: {}".format(bestScore))
      # print potential text
      print("==================================================================================")
      print("elapsed time: {}".format(time() - startTime))
      print("score: {}, key: {}".format(score, key))
      print("\t\tPotential Text: {}".format(xorResString))
      print("==================================================================================")

    if (key[currIndex] == 255):
      while (currIndex < i and key[currIndex] == 255):
        key[currIndex] = 0
        currIndex += 1
      if (currIndex == i):
        break
      key[currIndex] += 1
      currIndex = 0
    else:
      key[currIndex] += 1

  endTime = time()
  
  print("bestScore: {}".format(bestScore))
  print("Time taken: {}".format(endTime - startTime))

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
def calculateCharacterFrequency (string: str, onlyAlpha = True) -> dict:
  characterCounts = {}
  characterFrequency = {}

  for i in range(0, len(string), 2):
    charVal = int(string[i:i+2], 16)

    if (onlyAlpha):
      # ignore non letters
      if (charVal < 65 or (charVal > 90 and charVal < 97) or charVal > 122):
        continue

    if (onlyAlpha):
      # Make everything letter lowercase
      if (charVal >= 65 and charVal <= 90):
        charVal += 32

    if (onlyAlpha):
      char = chr(charVal)
    else:
      char = charVal

    if char in characterFrequency:
      characterCounts[char] += 1
      characterFrequency[char] = characterCounts[char] / (len(string) * 2)
    else:
      characterCounts[char] = 1
      characterFrequency[char] = 1 / (len(string) * 2)

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


# singleByteXor()

multiByteXor()


