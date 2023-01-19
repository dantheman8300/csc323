import base64 

## decoders/encoders

# encode strings to hexadecimal
def str_2_hex(s) -> str:
    return s.encode(encoding='UTF-8', errors='strict').hex()
# decode hexadecimal to strings
def hex_2_str(h) -> str:
    return bytes.fromhex(h).decode('utf-8', 'strict')
# decode base64 to hexadecimal
def base64_2_hex(b) -> str:
    return base64.b64decode(b).hex()
# encode hexadecimal to base64
def hex_2_base64(h) -> str:
    return base64.b64encode(bytes.fromhex(h)).decode()
# tests for decoders/encoders
# print(str_2_hex("a"))
# print(hex_2_str("68656C6C6F"))
# print(base64_2_hex("YQ=="))
# print(hex_2_base64("61"))



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

# tests for xor implementation
# print(xor("cat", "cat"))
# print(xor("cat", "ca"))
# print(xor("cat", "catt"))


def scorer():
    return 0

def single_byte_XOR():
    return 0

def multi_byte_XOR():
    return 0

def vigenere_cipher():
    return 0


# turn in as tar file!