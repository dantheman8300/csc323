from base64 import b64encode, b64decode
from time import sleep 
import matplotlib.pyplot as plt
from tqdm import tqdm

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

#===============================================================================
# Vigenere cipher helpers
#===============================================================================
def vigenereCipherEncrypt(plainText: str, key: str):
  plainText = plainText.lower()
  key = key.lower()
  cipherText = ""
  for i in range(0, len(plainText)):
    plainChar = plainText[i]
    keyChar = key[i % len(key)]
    keyOffset = ord(keyChar) - ord('a')
    cipherVal = ord(plainChar) + keyOffset
    if (cipherVal > ord('z')):
      cipherVal -= 26
    cipherChar = chr(cipherVal)
    cipherText += cipherChar
  return cipherText

def vigenereCipherDecrypt(cipherText: str, key: str):
  cipherText = cipherText.lower()
  key = key.lower()
  plainText = ""
  for i in range(0, len(cipherText)):
    cipherChar = cipherText[i]
    keyChar = key[i % len(key)]
    keyOffset = ord(keyChar) - ord('a')
    plainVal = ord(cipherChar) - keyOffset
    if (plainVal < ord('a')):
      plainVal += 26
    plainChar = chr(plainVal)
    plainText += plainChar
  return plainText

#===============================================================================


# Take in an ASCII encode string and key, and returns the XOR result in hex
# If the key is shorter than the plain text, it will be repeated
def xor (plain: str, key: str) -> str: 
  xorResHex = ""
  for i in range (0, len(plain)):
    plainChar = plain[i]
    keyChar = key[i % len(key)]
    xorCharInHex = str(hex(ord(plainChar) ^ ord(keyChar))).split('0x')[1].zfill(2)
    xorResHex += xorCharInHex
  return xorResHex

#===============================================================================
# Single byte XOR
#
#   Reads a list of 1000 hex encoded strings, where one of them is an english
#   plaintext that has been XORed with a single character. The program will find
#   the plaintext and output the plaintext, the ciphertext, and the xor key. 
# 
#   Note: The other 999 ciphertexts are random strings of hex encoded characters
#===============================================================================

def singleByteXor ():

  print("---Single Byte XOR---\n")
  sleep(0.5)

  # Read and parse the file
  btxt = open('Lab0.TaskII.B.txt', 'r').read().split('\n')
  btxt.pop()

  # Score tracker
  bestScore = -1
  ciphertext = ""
  xorKey = ""
  plaintext = ""

  # iterate through all ciphertexts, generate all posible plaintexts, and find
  # the one with the frequency score closest to the standard english frequencies
  for ciphertext in tqdm(btxt, "Cracking single byte XOR", leave=False):
    cipherXorResults = getAllSingleByteXorResults(ciphertext)
    for xorResult in cipherXorResults:
      charFreq = calculateCharacterFrequency(xorResult)
      freqScore = compareCharacterFrequencies(charFreq, STANDARD_FREQUENCIES)
      if (freqScore < bestScore or bestScore == -1):
        bestScore = freqScore
        plaintext = hexToString(xorResult)
        xorKey = xorResult[0]
        ciphertext = ciphertext
  
  print("\tScore: {}\n".format(bestScore))
  print("\tXOR Key:  \"{}\"\n".format(xorKey))
  print("\tPlaintext: \"{}\"\n".format(plaintext))
  print("\tCiphertext:  \"{}\"\n".format(ciphertext))

#===============================================================================
#===============================================================================
# Multi byte XOR
#
#   Takes a plaintext that has been XOR'd against a multi byte key of unknown 
#   length. The program will find the key length, and then find the key. Once 
#   the key is found, the program will decrypt the ciphertext and output the
#   plaintext, the ciphertext, the key, and the key length.
#===============================================================================

def multiByteXor():

  print("---Multi Byte XOR---\n")
  sleep(1)

  ctxt = open('Lab0.TaskII.C.txt', 'r').read().split('\n')
  ctxt.pop()
  ctxt = ''.join(ctxt)
  ctxt = hexToString(base64ToHex(ctxt))

  keyA = 'abcdefghijklmnopqrstuvwxyz'

  biggestDifferencePercentage = 0
  biggestDifferenceKeyLength = 0

  averageDifferencePercentages = []

  # Iterate through all possible key lengths and find the one with the highest
  # average difference percentage
  for i in range(1, len(keyA) + 1): 
    key = keyA[:i]
    strings = []
    for j in range(0, i):
      strings.append(ctxt[j::i])

    differencePercentageSum = 0

    for j in range(0, i):
      xorResult = xor(strings[j], key[j])
      differencePercentageSum += getCharacterPercentDifference(xorResult)

    averageDifferencePercentage = differencePercentageSum / i
    averageDifferencePercentages.append(averageDifferencePercentage)

    if (averageDifferencePercentage > biggestDifferencePercentage):
      biggestDifferencePercentage = averageDifferencePercentage
      biggestDifferenceKeyLength = i

  print("\tPercent difference: {:.2f}%".format(biggestDifferencePercentage))
  print("\tKey length: {}".format(biggestDifferenceKeyLength))

  plt.plot(range(1, len(keyA) + 1), averageDifferencePercentages)
  plt.xlabel("Key Length")
  plt.ylabel("Average Difference Percentage")
  plt.savefig("C.averageDifferencePercentages.png")
  plt.show()
  plt.clf()


  # Generate a list of all possible key values for each set of ciphertext
  numbers = []
  numbers.extend(range(0, 256))
  possibleKeyVals = []
  for i in range(0, biggestDifferenceKeyLength):
    possibleKeyVals.append(numbers.copy())

  # score trackers
  bestKeyValues = []
  bestKeyValueScores = []

  # Split the ciphertext into 5 sets to analyze the character distribution of 
  # each set. The key is the most common character in each set
  for i in range(biggestDifferenceKeyLength):
    cipherSubText = ctxt[i::biggestDifferenceKeyLength]
    bestKeyValue = -1
    bestKeyScore = -1
    for i in range(256):
      charFreq = calculateCharacterFrequency(xor(cipherSubText, chr(i)))
      charFreqScore = compareCharacterFrequencies(charFreq, STANDARD_FREQUENCIES)
      if (charFreqScore < bestKeyScore or bestKeyScore == -1):
        bestKeyScore = charFreqScore
        bestKeyValue = i
    
    bestKeyValues.append(bestKeyValue)
    bestKeyValueScores.append(bestKeyScore)

  xorKey = ''.join([chr(x) for x in bestKeyValues])
  print("Key: \"{}\"".format(xorKey))
  sleep(1)
  # print("Key score: {}".format(bestKeyValueScores))
  
  plaintext = hexToString(xor(ctxt, xorKey))
  print("Result: \"{}\"".format(plaintext))
  sleep(1)

#===============================================================================
#===============================================================================
# Vigenere Cipher
#
#   Take an ASCII encoded text that has been encrypted using the Vigenere Cipher
#   and decrypt it. The program will find the key length, and then find the key.
#   Once the key is found, the program will decrypt the ciphertext and output 
#   the plaintext, the ciphertext, the key, and the key length.
#=============================================================================== 

def vigenereCipher(): 

  print("---Vigenere Cipher---\n")
  sleep(1)

  dtxt = open('Lab0.TaskII.D.txt', 'r').read()
  print("dtxt: {}".format(dtxt))

  keyA = ''.join([chr(x) for x in range(20)]) # possible key values

  # Trackers
  biggestDifferencePercentage = 0
  biggestDifferenceKeyLength = 0
  differencePercentagesAverages = []

  # Iterate through all possible key lengths and find the one with the highest
  # average difference percentage
  for i in range(1, len(keyA) + 1):
    key = keyA[:i]
    strings = []
    for j in range(0, i):
      strings.append(dtxt[j::i])

    differencePercentageSum = 0

    for j in range(0, i):
      xorResult = xor(strings[j], key[j])
      differencePercentageSum += getCharacterPercentDifference(xorResult)

    averageDifferencePercentage = differencePercentageSum / i
    differencePercentagesAverages.append(averageDifferencePercentage)

    if (averageDifferencePercentage > biggestDifferencePercentage):
      biggestDifferencePercentage = averageDifferencePercentage
      biggestDifferenceKeyLength = i


  print("\tPercent difference: {:.2f}%".format(biggestDifferencePercentage))
  print("\tKey length: {}".format(biggestDifferenceKeyLength))

  plt.plot(range(1, len(keyA) + 1), differencePercentagesAverages)
  plt.xlabel("Key Length")
  plt.ylabel("Average Difference Percentage")
  plt.savefig("D.averageDifference.png")
  plt.show()
  plt.clf()

  # Generate a list of all possible key values for each set of ciphertext
  numbers = []
  numbers.extend(range(0, 256))
  possibleKeyVals = []
  for i in range(0, biggestDifferenceKeyLength):
    possibleKeyVals.append(numbers.copy())

  # score trackers
  bestKeyValues = []
  bestKeyValueScores = []

  # Split the ciphertext into 5 sets to analyze the character distribution of 
  # each set. The key is the most common character in each set  
  for i in range(biggestDifferenceKeyLength):
    cipherSubText = dtxt[i::biggestDifferenceKeyLength]
    bestKeyValue = -1
    bestKeyScore = -1
    for i in range(97, 123):
      charFreq = calculateCharacterFrequency(stringToHex(vigenereCipherDecrypt(cipherSubText, chr(i))))
      charFreqScore = compareCharacterFrequencies(charFreq, STANDARD_FREQUENCIES)
      if (charFreqScore < bestKeyScore or bestKeyScore == -1):
        bestKeyScore = charFreqScore
        bestKeyValue = i
    
    bestKeyValues.append(bestKeyValue)
    bestKeyValueScores.append(bestKeyScore)

  print("bestKeyValues: \"{}\"".format(bestKeyValues))
  # print("bestKeyValueScores: {}".format(bestKeyValueScores))
  xorKey = ''.join([chr(x) for x in bestKeyValues])
  print("xorKey: \"{}\"".format(xorKey))
  print("Result: \"{}\"".format(vigenereCipherDecrypt(dtxt, xorKey)))

  sleep(2)

#===============================================================================
#===============================================================================
# Helper Functions
#===============================================================================

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

# Returns a list of all possible single byte xor results
def getAllSingleByteXorResults (string: str) -> list:
  xorResults = []

  # Generate all possible single byte xor results
  for i in range(0, 256):
    xorResults.append(xor(hexToString(string), chr(i)))

  return xorResults

# Returns percent difference between the most and least common characters of the 
# given string
def getCharacterPercentDifference (string: str) -> float:
  freq = calculateCharacterFrequency(string, False)
  difference = max(freq.values()) - min(freq.values())
  freqSum = sum(freq.values())
  averageDifference = difference / freqSum * 100
  return averageDifference
  
#===============================================================================
#===============================================================================
# Encoding/Decoding helpers
#===============================================================================

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

#===============================================================================

singleByteXor()

print("\n\n\n")
sleep(6)

multiByteXor()

print("\n\n\n")
sleep(6)

vigenereCipher()
