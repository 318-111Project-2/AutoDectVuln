import angr
from pwn import *
from lib.Tool import *

def print_result(act: angr.sim_state.SimState) -> None:
    ret_addr = act.callstack.ret_addr
    block=act.project.factory.block(ret_addr)
    func_addr=act.globals['func_block_addr'][block.addr]

    # get function name
    cfg = act.globals['cfg']
    func = cfg.kb.functions[func_addr]

    # do write to report file
    do_write(f'[*]heap_over_flow found in function: {func.name}\n')
    do_write(f'    === Process ===\n')
    for addr in act.history.bbl_addrs:
        try:
            do_write(f'    {cfg.kb.functions[addr].name}\n')
        except:
            pass
    do_write(f'    ===============\n\n')

    VULN_DICT["HeapOverFlow"] += 1

def check_malloc(act):
    info(f'I will check malloc. in {hex(act.addr)}')

    # get first parameter address of malloc
    Arg=act.project.factory.cc().ARG_REGS[0]
    first_param=act.solver.eval(act.regs.get(Arg))
    act.globals['malloc_size']=first_param

def check_mem_write(state):
    if state.inspect.mem_write_address == None:
        return
    
    # get write address and size
    write_addr = state.solver.eval(state.inspect.mem_write_address)
    write_size = state.inspect.mem_write_length

    # check if write address in malloc_addr
    if write_addr in list(state.globals['malloc_addr'].keys()):
        if type(write_size) != int:
            write_size = state.solver.eval(write_size)
            
        # check if write size > malloc size
        if write_size > state.globals['malloc_addr'][write_addr]:
            print(write_size)
            print("find heap overflow")
            print('write', 'from', state.inspect.mem_write_address)
            print_result(state)

def check_mem_read(state):
    if state.inspect.mem_read_address == None:
        return
    
    # get read address and size
    read_addr = state.solver.eval(state.inspect.mem_read_address)
    read_size = state.inspect.mem_read_length

    # check if read address in malloc_addr
    if read_addr in list(state.globals['malloc_addr'].keys()):
        if type(read_size) != int:
            read_size = state.solver.eval(read_size)

        # check if read size > malloc size
        if read_size > state.globals['malloc_addr'][read_addr]:
            print(read_size)
            print("find heap overflow")
            print('read', 'from', state.inspect.mem_read_address)
            print_result(state)

def HeapOverFlow(proj):
    # binary process
    initial_state = proj.factory.entry_state(
        add_options = { 
            angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY,
            angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS
        }
    )

    cfg = proj.analyses.CFGFast()

    # if you want to use cfg in other function, you need to add this line
    initial_state.globals['cfg']=cfg

    initial_state.globals['func_block_addr']={}
    initial_state.globals['find_malloc_flag']=False
    initial_state.globals['malloc_addr']={}
    initial_state.globals['malloc_size']=0

    # add breakpoint
    initial_state.inspect.b('mem_write', when=angr.BP_AFTER, action=check_mem_write)
    initial_state.inspect.b('mem_read', when=angr.BP_AFTER, action=check_mem_read)


    # main exlpore
    simgr = proj.factory.simgr(initial_state)
    while simgr.active:
        for act in simgr.active:

            # get rax after call malloc
            if act.globals['find_malloc_flag']==True:
                    rax = act.solver.eval(act.regs.rax)
                    act.globals['malloc_addr'][rax]=act.globals['malloc_size']
                    act.globals['find_malloc_flag']=False

            '''
                check first parameter of "malloc" 
            '''
            try:
                # print(act.addr)
                func = cfg.kb.functions[act.addr]

                # get function block address
                block_addrs=list(func.block_addrs)
                for block_addr in block_addrs:
                    act.globals['func_block_addr'][block_addr]=act.addr

                
                act.globals['find_malloc_flag']=False
                # print(func.name)
                if func.name == 'malloc':

                    # 避免檢查simprocedures
                    block = act.project.factory.block(act.addr)
                    if block.instructions <=2:
                        continue
                    check_malloc(act)
                    act.globals['find_malloc_flag']=True
            except:
                pass
        simgr.step()     