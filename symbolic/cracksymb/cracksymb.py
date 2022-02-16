import binascii
import claripy
import angr

#in order to install binascii and claripy on python3, I need to write on the terminal:
#python3 -m pip install angr

#I want to entry in the correct puts, because it would mean I have the flag
find_address = 0x4033bb
avoid_address = 0x4033c9

p = angr.Project('cracksymb')

flag = claripy.BVS('flag', 0x17*8)

st = p.factory.full_init_state(
    args=['./cracksymb'],
    add_options={angr.options.LAZY_SOLVES},
    stdin=angr.simos.simos.SimFileStream(name='stdin', content=flag, has_end=False),
)

sm = p.factory.simulation_manager(st)
sm.explore(find=find_address, avoid=avoid_address)

try:
    p = sm.found[0]

    sol = p.solver.eval(flag, cast_to=bytes)
    print(b"Solution found: " + sol)
except Exception as e:
    print('unsat', e)