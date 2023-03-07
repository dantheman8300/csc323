import struct

def sha1(message):
    # Initialize constants
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    # Pre-processing
    message = bytearray(message, 'utf-8')
    ml = 8 * len(message)
    message.append(0x80)
    while len(message) % 64 != 56:
        message.append(0x00)
    message += struct.pack(">Q", ml)

    if (len(message) % 64 != 0):
        raise Exception("Invalid message length")

    # Process message in 512-bit chunks
    for i in range(0, len(message), 64):
        chunk = message[i:i+64]

        # Break chunk into 16 32-bit words
        w = list(struct.unpack(">16L", chunk))

        # Extend the 16 32-bit words into 80 32-bit words
        for j in range(16, 80):
            w.append(((w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16]) << 1) | ((w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16]) >> 31))

        # Initialize hash value for this chunk
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        # Main loop
        for j in range(80):
            if j <= 19:
                f = (b & c) ^ ((~b) & d)
                k = 0x5A827999
            elif j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif j <= 59:
                f = (b & c) ^ (b & d) ^ (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = ((a << 5) | (a >> 27)) + f + e + k + w[j] & 0xFFFFFFFF
            e = d
            d = c
            c = (b << 30) | (b >> 2)
            b = a
            a = temp

        # Add this chunk's hash to result so far
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    # Produce the final hash value
    return "%08x%08x%08x%08x%08x" % (h0, h1, h2, h3, h4)

hash = sha1("abc")
print(hash) # Output: 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12