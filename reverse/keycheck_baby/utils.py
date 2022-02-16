import binascii

#THIS FILE IS CALLED utils.py AND NOT keycheck_baby.py BECAUSE IT IS NOT A SCRIPT!
#IT HAS BEEN USED JUST TO MAKE CALCULATIONS IN ORDER TO RETRIEVE THE FLAG FOR THIS CHALLENGE

#flag: flag{y0u_d4_qu33n_0f_cr4ck1ngz}


#we have to find the correct flag for the challenge
#we have to face two checks in order to pass the challenge without being sent to the end of the code


#first check:

#for (i = 0; i < 13; i = i + 1) {
#        if ((byte)(local_80[(int)i] ^ "babuzz"[(ulong)(long)(int)i % 6]) != magic0[(int)i])
#        goto LAB_00101487;
#      }


#I need to confront byte per byte the string "babuzz"
#str = binascii.hexlify(b"babuzz"[::-1]) 
#I reverse the string because I need its little endian version
#print(str)
#we have that babuzz is 0x7a7a75626162

#babuzz = "babuzz"
#for i in range(13):
#    print(babuzz [i % 6] )
#it prints babuzzbabuzzb, so I have to confront with concatenated: 0x7a7a75626162 0x7a7a75626162 0x62

#now I need the content of magic0, it is located at the address 0x555555556028
#the content is 0x103d4e1e2a17511b	0x6261623d14494617

#in order to get what I have to write, I have to execute the inverse operation of the xor, that is.. xor!
def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

#babuzzbabuzzb: 0x7a7a75626162 0x7a7a75626162 0x7a7a75626162 (but of this last one I will just confront 0x62)
#magic0: 0x103d4e1e2a17511b	0x6261623d14494617
#I have to confront them as 62^1b, 61^51 etc... so, starting from the last byte even if they have byte of different lenght..
#continuing in this way, I will confront 62^3d restarting with the second group of bytes of the second babuzz, concluding with 62^3d
#byte_result = byte_xor(b'\x62', b'\x1b') is the first step
#byte_result = byte_xor(b'\x62', b'\x3d') is the last step
#print(byte_result)

#so far, I got: flag{y0u_d4_qu33n_}



#second check:

      #local_80 = local_80 + 13;  #this line is needed to get the second part of the flag
      #local_85 = -69;
      #for (i = 0; i < 12; i = i + 1) {
      #  local_85 = local_85 + *local_80;
      #  local_80 = local_80 + 1;
      #  if (local_85 != magic1[(int)i]) goto LAB_00101487;
      #}

#magic1 - local_85 =  local_80


#now I need the content of magic1, it is located at the address 0x555555556040
#the content is 0x871cb98513b051eb	0x67616c66078d26b8

#I need that local_85 == magic1[i] for 12 times
#the first byte of magic1, so magic1[0] is '\xeb', so I want to insert a byte such that '\xeb' = local_85 + inserted_byte,
#so inserted_byte needs to be '\xeb' - local_85, and at the beginning local_85 is initialized as -69

#I saw that local_85 is initialized with -69, that, seen with gdb, is converted to a char as '\xbb'.
#so I need to insert a value x    s.t.    x + '\xbb' = '\xeb'
#I need to calculate the value as a module since it is codified as a unicode(/ASCII) value, and there are 256 values of characters in the ASCII and unicode tables

print((chr)((0xeb - 0xbb) % 256)) #0
print((chr)((0x51 - 0xeb) % 256)) #f
print((chr)((0xb0 - 0x51) % 256)) #_
print((chr)((0x13 - 0xb0) % 256)) #c
print((chr)((0x85 - 0x13) % 256)) #r
print((chr)((0xb9 - 0x85) % 256)) #4
print((chr)((0x1c - 0xb9) % 256)) #c
print((chr)((0x87 - 0x1c) % 256)) #k
print((chr)((0xb8 - 0x87) % 256)) #1
print((chr)((0x26 - 0xb8) % 256)) #n
print((chr)((0x8d - 0x26) % 256)) #g
print((chr)((0x07 - 0x8d) % 256)) #z

#second part of the flag: 0f_cr4ck1ngz


#whole flag: flag{y0u_d4_qu33n_0f_cr4ck1ngz}