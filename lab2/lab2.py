from Crypto.Cipher import AES
import base64


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



file_e = open("lab2\Lab2_TaskII_A.txt", 'rb')
f_out = open("lab2\out.txt", "wb")
# ebc_encrypt(b'1234567812345678', file_e, f_out)
file_e.close()
f_out.close()

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


file_b = open("lab2\Lab2.TaskII.B.txt", "r")
read_BMPs(file_b.readlines())


## TASK II:  ECB Cookies