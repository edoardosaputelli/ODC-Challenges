def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

byte_result = byte_xor(b'&', b'\x0b')
byte_result = byte_xor(b'-', b'\x4c')
byte_result = byte_xor(b'a', b'\x0f')
byte_result = byte_xor(b'n', b'\x00')
byte_result = byte_xor(b'n', b'\x01')
byte_result = byte_xor(b'o', b'\x16')
byte_result = byte_xor(b'y', b'\x10')
byte_result = byte_xor(b'i', b'\x07')
byte_result = byte_xor(b'n', b'\x09')
byte_result = byte_xor(b'g', b'\x38')
byte_result = byte_xor(b'_', b'\x00')
byte_result = byte_xor(b'_', b'\x00')
print(byte_result)

#flag{packer-4_3-1337&-annoying__}