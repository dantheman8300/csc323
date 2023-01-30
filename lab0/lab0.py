import base64 

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



# task 2 part A
## Implement XOR 
# if key < plaintext -> repeat key
def xor(p, k) -> str:
    result = ""
    y = 0
    if(len(k) < len(p)):
        for x in p:
            result += chr(ord(x) ^ ord(k[y % len(k)]))
            y += 1
    else:
        for x in p:
            result += chr(ord(x) ^ ord(k[y]))
            y += 1
    return str_2_hex(result)



## task 1 - decoders/encoders
# encode strings to hexadecimal
def str_2_hex(s) -> str:
    return s.encode(encoding='UTF-8', errors='strict').hex()
# decode hexadecimal to strings
def hex_2_str(h) -> str:
    result = ""
    for i in range(0, len(h) - 1, 2):
        result += chr(int(h[i:i+2], 16))
    return result
# decode base64 to hexadecimal
def base64_2_hex(b) -> str:
    return base64.b64decode(b).hex()
# encode hexadecimal to base64
def hex_2_base64(h) -> str:
    return base64.b64encode(bytes.fromhex(h)).decode()




## helper functions
# checks if s is a letter
def isLetter(s):
    if((s >= 'A' and s <= 'Z') or (s >= 'a' and s <= 'z') or s== ' '):
        return True
    return False

# checks if s is an ascii printable character
def isPrintable(s):
    if(s >= ' ' and s <= '~'):
        return True
    return False



# count occurance of letters - frequency analysis
def freq_analysis(mes, mode = 0):
    chars =  {} 
    for s in mes:
        if(mode == 1):
            if(isPrintable(s)):
                # lower case
                # s = s.lower()
                if(s in chars):
                    chars[s] += 1
                else :
                    chars[s] = 1

        # ignore non letters
        else:
            if(isLetter(s)):
                # lower case
                s = s.lower()
                if(s in chars):
                    chars[s] += 1
                else :
                    chars[s] = 1

    # calculate ratio of amt of each character
    for i in chars:
        chars[i] = chars[i] / (len(mes) * 2) # * 2 ??

    return chars

# compare calculated frequencies to standard frequencies
def scorer(chars, std):
    # total = prob of letter relation
    total = 0

    # iterate through avail characters
    for i in chars:
        #if is in standard add to total
        if i in std:
            total += abs(chars[i] - std[i])
        else:
            total += chars[i]

    for i in std:
        if i not in chars:
            total += std[i]
    return total



# task 2 part B
def single_byte_XOR(cipher):

    # decode string
    txt = hex_2_str(cipher)
    # xor message for each ascii value -> hex
    result = [0] * 255
    for key in range(255):
        result[key] = xor(txt, chr(key))

    currentScore = 10000
    index = 0
    # result to string, score c -> figure out high score
    for c in range(len(result)):
        xord = hex_2_str(result[c])
        freq = freq_analysis(xord)
        score = scorer(freq, STANDARD_FREQUENCIES)

        if(score < currentScore):
            currentScore = score
            index = c
    try:
        return hex_2_str(result[index])
    except:
        return None

# f = open("csc323\lab0\Lab0_TaskII_B.txt", "r")
# out = open("csc323\lab0\out.txt", "w")
# cipher = f.readlines()

# for i in cipher:
#     try:
#         out.write(single_byte_XOR(i))
#         break
#     except:
#         continue

# out.close()
# f.close()


def grabIntervalStr(interval, txt):
    n = [0] * interval
    for i in range(interval):
        x = slice(i,len(txt),interval)
        n[i] = txt[x]
    return n


def scorer2(txt):
    key = "abcdefghijklmnopqrst"
    max = -1
    length = -1
    good = ""
    for size in range(len(key)):
        k = key[0:size+1]
        x = xor(txt, k)
        xord = hex_2_str(x)
        arrs= grabIntervalStr(len(key), xord)
        
        freqs = [0] * len(arrs)
        ind = 0
        for y in arrs:
            freqs[ind] = freq_analysis(y, 1)
            ind += 1


        for amt in freqs:
            min = 1000
            most = -1
            for num in amt:
                if(amt[num] < min):
                    min = amt[num]
                elif(amt[num] > most):
                    most = amt[num]
        
        if(abs(most - min) > max):
            max = abs(most - min)
            length = len(k)
    return length


# task 2 part C
def multi_byte_XOR(cipher, out):

    # decode from base 64 -> hex -> str
    txt = hex_2_str(base64_2_hex(cipher))
    length = scorer2(txt)
    arr = grabIntervalStr(length, txt)
    best = [0, 0, 0, 0, 0]
    ind = 0
    for s in arr:
        currentScore = 10000
        value = 0
        for i in range(255):
            x = xor(s, chr(i))
            xord = hex_2_str(x)
            freq = freq_analysis(xord)
            score = scorer(freq, STANDARD_FREQUENCIES)

            if(score < currentScore):
                currentScore = score
                value = i
        best[ind] = chr(value)
        ind += 1
        
    key = ""
    for i in best:
        key += i

    x = xor(txt, key)
    result = hex_2_str(x)
    # print(result)
    try:
        out.write(result)
    except:
        print("sad")

# f = open("csc323\lab0\Lab0_TaskII_C.txt", "r")
# out = open("csc323\lab0\out2.txt", "w")
# cipher = f.read()
# multi_byte_XOR(cipher, out)


# task 2 part D
def vigenere_cipher():
    return 0



