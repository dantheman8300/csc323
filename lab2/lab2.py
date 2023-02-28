from Crypto.Cipher import AES
import base64
import requests







## TASK I: PADDING FOR BLOCK CIPHERS
# implement pkcs#7
# 01 -- if lth mod k = k-1
# 02 02 -- if lth mod k = k-2
#           .
#           .
#           .
# k k ... k k -- if lth mod k = 0

# ie amt to pad = k - (l % k)
# l = size of text
def pad(txt):
    k = 16 # block size
    l = len(txt)
    pad_amt = k - l
    for _ in range(pad_amt):
        txt += pad_amt.to_bytes(1, "big")
    return txt

# Be sure to throw an exception (or return an error) 
# in the unpad() function if it receives an input 
# with invalid padding 
# Be sure to test your implementation, including validating EVERY BYTE of the padding,
#  as well as its behavior if the message is a multiple of the block size
def unpad(txt):
    pad_amt = txt[-1]
    barr = bytearray(txt)
    for _ in range(pad_amt):
        if(barr[-1] != pad_amt):
            
            raise ValueError('Invalid padding.')
        barr.pop()
    return bytes(barr)


## TASK II: ECB MODE

# implement ecb mode
# takes in a 128-bit key 
# an arbitrary-length plaintext, 
# pads the message to multiple of the block size
# pt = file stream
def ebc_encrypt(key, pt, out):
    block = pt.read(16)
    while(len(block) > 0):
        block = pad(block)
        cipher = AES.new(key, AES.MODE_ECB)

        block_cipher = cipher.encrypt(block)
        out.write(block_cipher)

        block = pt.read(16)




# take in a ciphertext and a key, 
# decrypt the ciphertext, 
# remove the padding, 
# and return the resulting plaintext
def ecb_decrypt(cipher, key, out):
    block = cipher.read(16)
    while(len(block) > 0):
        aes = AES.new(key, AES.MODE_ECB)
        block_decipher = aes.decrypt(block)

        block = cipher.read(16)
        if(len(block) == 0):
            txt = unpad(block_decipher)
            out.write(txt)
        else:
            out.write(block_decipher)

# decode hexadecimal to strings
def hex_2_str(h) -> str:
    result = ""
    for i in range(0, len(h) - 1, 2):
        result += chr(int(h[i:i+2], 16))
    return result

## TASK II : identify ECB mode
# 100 hex encoded bmp files
def detect_ecb():
    return 0


def read_BMPs(file):
    for i in range(len(file)):
        hex_decode = open("lab2\decode_hex"+ str(i+1) + ".bmp", "wb")
        line = file[i].rstrip('\n')
        hex_decode.write(bytes.fromhex(line))
        hex_decode.close()

def read_in_blocks(cipher):
    blocks = {}
    block = cipher.read(16)
    while(len(block) > 0):
        val = int.from_bytes(block, 'big')
        if(blocks.get(val) != None):
            blocks[val] += 1
        else:
            blocks.update({val : 1})
        block = cipher.read(16)
    return blocks


def score_BMPs():
    score = [0] * 100
    ind = 0
    for val in range(100):
        cipher = open("./decode_hex"+ str(val+1) + ".bmp", "rb")
        blocks = read_in_blocks(cipher)

        score[ind] = len(blocks)
        ind+=1

    min = score[0]
    ind = 0
    winner = 0
    for i in score:
        if i < min:
            min = i
            winner = ind + 1
        ind += 1

    print(winner)
    


## TASK II:  ECB Cookies
# create a valid cookie that gives admin access
# user=USERNAME&uid=UID&role=ROLE

# user=aaaaaaaaaaa
# user************
# admin***********
# user************
# aaa&uid=aa&role=
# admin***********

def ECB_Cookies():
    session = requests.Session()
    url = 'http://localhost:8080/register'
    url2 = 'http://localhost:8080/'
    url3 = 'http://localhost:8080/home'
    username = "12345678912"+"user\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0C"+"admin\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0B"+"user\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0C" + "1234"
    password = 'a'

    # register
    z = session.post(url, {"user" : username, "password" : password})

    # login
    y = session.post(url2, {"user" : username, "password" : password})

    # get cookie on home page
    x = session.get(url3)
    cookie = session.cookies['auth_token']


    arr = [0] * int((len(cookie)/ 32))
    ind = 0
    for i in range(0, len(cookie), 32):
        arr[ind] = cookie[i:i+32]
        ind+=1

    print("Current Cookie:")
    for index in arr:
        print(index)

    print("Attack Cookie: ")
    admin = arr[2]
    attack = ''
    for i in range(len(arr)):
        if i == 5:
            attack += admin
            print(admin)
        else:
            attack += arr[i]
            print(arr[i])
    print()
    print(attack)





def xor(a, b):
    xorBytes = b''

    for i in range(len(a)):
        xorBit = a[i]^b[i]
        xorBitByte = xorBit.to_bytes(1, 'big')
        xorBytes += xorBitByte

    return xorBytes


## TASK III: CBC

def encrypt_cbc(file, out, iv, key=b'1234567812345678',  bmp = False):
  # Read input file
    fileIn = open(file, "rb")
    if (bmp):
        headerBytes = fileIn.read(54) # store header info

    # Create output file
    fileOut = open(out, 'wb')
    if (bmp):
        fileOut.write(headerBytes)

    # Read first block of data
    block = fileIn.read(16)
    padded = False

    # gernerate IV
    prevCipherText = str.encode(iv)
    fileOut.write(str.encode(iv))
    while(len(block) > 0):
    # create aes cipher
        cipher = AES.new(key, AES.MODE_ECB)

        if(len(block) < 16):
            block = pad(block)
            padded = True

        blockCipherText = cipher.encrypt(xor(block, prevCipherText))
        fileOut.write(blockCipherText)

        prevCipherText = blockCipherText
        block = fileIn.read(16)

    # add full padded block if needed
    if (not padded):
        block = pad(b'')
        cipher = AES.new(key, AES.MODE_ECB)
        blockCipherText = cipher.encrypt(xor(block, prevCipherText))
        fileOut.write(blockCipherText)

    return iv

def decrypt_cbc(file, out, iv, key):
    # Read input file
    fileIn = open(file, "rb")

    # Create output file
    fileOut = open(out, 'wb')

    # Read first block of data
    iv = fileIn.read(16)
    block = fileIn.read(16)

    # gernerate IV
    prevCipherText = iv
    # i=0
    while(len(block) > 0):
        # print(i)
        # i+=1
        # create aes cipher
        cipher = AES.new(key, AES.MODE_ECB)

        blockCipherText = xor(cipher.decrypt(block), prevCipherText)
        # fileOut.write()

        prevCipherText = block
        block = fileIn.read(16)
        print(len(block))
        if(len(block) == 0):
            txt = unpad(blockCipherText)
            fileOut.write(txt)
        else:
            fileOut.write(blockCipherText)

    return iv

# iv**************
# user=aaaaaaaaaa& \x26
# useraaaaaaaaaaa&
# useraaaaaaaaaaa&
# ****************
# ****&uid=U&role=
# admin***********


# iv**************
# user=1234567891&
# uid=1&role=userx

# 8a7b7d3dc959118d004b946a8ad1e48a
# 40ae0f612bfff66ea80355b44d4332dc
# feb0dd79638ef3a2a56ed4488b4a91f4

def CBC_Cookies():
    session = requests.Session()
    url = 'http://localhost:8080/register'
    url2 = 'http://localhost:8080/'
    url3 = 'http://localhost:8080/home'
    username = '12345678912' + '12345678912345'
    attackU = '1234'
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

    cookie[9 + 16 * 0]  ^= ord('5') ^ ord('&')
    cookie[10 + 16 * 0] ^= ord('6') ^ ord('u')
    cookie[11 + 16 * 0] ^= ord('7') ^ ord('i')
    cookie[12 + 16 * 0] ^= ord('8') ^ ord('d')
    cookie[13 + 16 * 0] ^= ord('9') ^ ord('=')
    cookie[14 + 16 * 0] ^= ord('1') ^ ord('6')
    cookie[15 + 16 * 0] ^= ord('2') ^ ord('&')

    cookie[0 + 16 * 2]  ^= ord('1') ^ ord('&')
    cookie[10 + 16 * 2] ^= ord('u') ^ ord('a')
    cookie[11 + 16 * 2] ^= ord('s') ^ ord('d')
    cookie[12 + 16 * 2] ^= ord('e') ^ ord('m')
    cookie[13 + 16 * 2] ^= ord('r') ^ ord('i')
    cookie[14 + 16 * 2] ^= ord('\x00') ^ ord('n')
    cookie[15 + 16 * 2] ^= ord('\x02') ^ ord('\x01')

    cookie = cookie.hex()

    # print attacked cookie in blocks of 16 bytes
    print("Attacked Cookie: ")
    for i in range(0, len(cookie), 32):
        print(cookie[i:i+32])


    print('attacked cookie: {}'.format(cookie))






def task2_encrypt():
    file_e = open("lab2\Lab2_TaskII_A.txt", 'rb')
    f_out = open("lab2\out.txt", "wb")
    # ebc_encrypt(b'1234567812345678', file_e, f_out)
    file_e.close()
    f_out.close()


def task2a():
    file_d = open("lab2\Lab2_TaskII_A.txt", 'r')

    cipher = open("lab2\decode.txt", "wb")
    cipher.write(base64.b64decode(file_d.read()))
    cipher.close()

    ct = open("lab2\decode.txt", "rb")
    f_out2 = open("lab2\out2.txt", "wb")
    ecb_decrypt(ct, b'CALIFORNIA LOVE!', f_out2)
    ct.close()
    file_d.close()
    f_out2.close()

def task2b():
    file_b = open("./Lab2.TaskII.B.txt", "r")
    lines = file_b.readlines()
    # read_BMPs(lines)
    score_BMPs()

# run server.py
def task2c():
    ECB_Cookies()


def task3_encrypt():

    encrypt_cbc("decode_hex22.bmp", "mustang-e-cbc.txt", b"MONEY ON MY MIND")


def task3_decrypt():
    file_d = open("Lab2.TaskIII.A.txt", 'r')
    cipher = open("decode_3.txt", "wb")
    cipher.write(base64.b64decode(file_d.read()))
    cipher.close()
    decrypt_cbc("decode_3.txt", "decrypt_cbc.txt", b'MONEY ON MY MIND', b'MIND ON MY MONEY')

# run server.py
def task3_cookies():
    CBC_Cookies()

task2c()