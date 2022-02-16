from pwn import *

#solution retrieved with the angr_utils.py script: 
#M4@@9-8  7@-@@@9 -6@BB2-@@ 88

#to retrieve the flag is enough to pass the solution to the r.interactive()

r = remote("bin.training.jinblack.it", 2021)
r.interactive()

#flag{nice_keygen!now_it_only_needs_some_music!_notleakedflag}