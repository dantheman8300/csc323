
## TASK 1: PADDING FOR BLOCK CIPHERS

# implement pkcs#7


# 01 -- if lth mod k = k-1
# 02 02 -- if lth mod k = k-2
#           .
#           .
#           .
# k k ... k k -- if lth mod k = 0

# ie amt to pad = k - (l % k)

def pad(k, l, txt):
    if(k < 256 and k > 1):
        amt = k - l % k
        n = txt
        for i in range(amt):
            n += 
    return 0

# Be sure to throw an exception (or return an error) 
# in the unpad() function if it receives an input 
# with invalid padding 
# Be sure to test your implementation, including validating EVERY BYTE of the padding,
#  as well as its behavior if the message is a multiple of the block size
def unpad():
    return 0


f = open('csc323\lab2\Lab2.TaskII.A.txt', 'r')
txt = f.read()
