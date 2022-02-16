import sys
from pwn import u32, p32

if len(sys.argv) < 4:
    print("usage : %s <inputfile> <address> <size>" % sys.argv[0])
    exit(0)

filepath = sys.argv[1]
address = int(sys.argv[2], 16)
size = int(sys.argv[3], 16)

#we don't need to pass a variable offset to the argv parameters since the function passed as a parameter is at the beginning of the section,
#address of the beginning of the section:
BEG_BIN = 0x08048000

#values of the keys retrieved from the global variable of Ghidra, pay attention to the endianness
KEY = [0x04030201, 0x40302010, 0x42303042, 0x44414544, 0xffffffff]

ff = open(filepath, "rb")
f = ff.read() #extracting the file I want to decrypt
ff.close()

off = address - BEG_BIN
#I want to decode from off to off+(size*4) (in the unpack function I iterate for 4 bytes everytime)
to_decode = f[off: off+(size*4)]
k = KEY[address % 5]

decode = b""
for i in range(size):
    decode += p32(u32(to_decode[i*4: (i+1)*4]) ^ k)

#in order to create the original file:
f = f[:off] + decode + f[off+(size*4):]

#now I need to write it
ff = open(filepath, "wb")
ff.write(f)
ff.close()
