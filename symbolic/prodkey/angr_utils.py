import binascii
import claripy
import angr

find_address = 0x00400e58
avoid_address = 0x00400e73

#creating the project
proj = angr.Project('prodkey')

#I need 30 bytes since the constraints, saw on the Ghidra code, need at least 29 chars
chars = [claripy.BVS('c%d' % i, 8) for i in range(30)]
input_str = claripy.Concat(*chars + [claripy.BVV(b'\n')])


#defining the initial state, passing the input_str as content
st = proj.factory.full_init_state(
    args=['./prodkey'],
    #add_options={angr.options.LAZY_SOLVES},
    stdin=angr.simos.simos.SimFileStream(name='stdin', content=input_str, has_end=False),
)

#characters needs to be printable!!!!!!!
for c in chars:
    st.solver.add(c >= 0x20, c<=0x7e)

#defining and initializing the simulation manager
simgr = proj.factory.simulation_manager(st)
simgr.explore(find=find_address, avoid=avoid_address)


try:
    print(simgr.found[0].posix.dumps(0))

    p = simgr.found[0]
    sol = p.solver.eval(input_str, cast_to=bytes)
    print(b"Solution found: " + sol)

except Exception as e:
    print('unsat', e)


#solution retrieved with angr:
#M4@@9-8  7@-@@@9 -6@BB2-@@ 88