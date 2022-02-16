import z3
from IPython import embed
from pwn import *

#pay attention: you have to run it with "python prng.py", and not python3!

#r = process("./pnrg")
r = remote("training.jinblack.it",  2020)

class State:
    def __init__(self):
        self.state = [0]*0x270
        self.index = 0

def mag(i):
     return z3.If(i==0, z3.BitVecVal(0x0,32 ), z3.BitVecVal(0x9908b0df,32 ))

def seedRand( s , seed):
    s.state[0] = seed & 0xffffffff
    s.index = 1
    while s.index < 0x270:
        s.state[s.index] = (s.state[s.index- 1] * 0x17b5)& 0xffffffff
        s.index= s.index + 1
    return s

def rss(a,b):
    return z3.LShR(a,b)


def getRandLong(s):
  if ((0x26f < (s.index)) or ((s.index) < 0)):

    if ((0x270 < (s.index)) or ((s.index) < 0)):
        seedRand(s,0x1105)

    for i in range(0xe3):
        s.state[i] = (s.state[i + 0x18d] ^ (rss((s.state[i + 1] & 0x7fffffff | s.state[i] & 0x80000000), 1)) ^ mag(s.state[i + 1] & 1)) & 0xffffffff

    for i in range(0xe3,0x26f):
        s.state[i] = (s.state[i + -0xe3] ^ (rss((s.state[i + 1] & 0x7fffffff | s.state[i] & 0x80000000), 1))^ mag(s.state[i + 1] & 1)) & 0xffffffff


    s.state[0x26f] = (s.state[0x18c] ^ ((s.state[0] & 0x7fffffff | s.state[0x26f] & 0x80000000) >> 1) ^ mag(s.state[0] & 1) )& 0xffffffff
    s.index = 0
  
  j = s.index
  s.index = j + 1
  uVar2 = (s.state[j] ^ rss(s.state[j],0xb) )& 0xffffffff
  uVar2 = (uVar2 ^ (uVar2 << 7) & 0x9d2c5680)& 0xffffffff
  uVar2 = (uVar2 ^ (uVar2 << 0xf) & 0xefc60000)& 0xffffffff
  rnd = (uVar2 ^ rss(uVar2 , 0x12))& 0xffffffff
  return s, rnd


#------------main:

seed = z3.BitVec('seed',32)

s = State()
s = seedRand(s, seed)

for i in range(1000):
    s, n= getRandLong(s)
    
s, output = getRandLong(s)


INPUT = r.recvuntil(',').strip(',')
INPUT = int(INPUT, 16)



r.recvuntil("guess the seed:")

#----- solving:
solver = z3.Solver()
solver.add( output==INPUT )
print("Solving...")
solver.check()
e = solver.model()

result = str(e)
seed = int(result[8:17])

r.sendline(str(seed))

#flag{you_can_easly_break_non_crypto_fun!}
