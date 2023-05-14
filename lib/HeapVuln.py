import angr
from pwn import *
from lib.Tool import *

def print_result(act: angr.sim_state.SimState) -> None:
    # get module name and add vuln count
    module_name = "heap_over_flow"
    if act.globals['module'] == 'HeapOverFlow':
        VULN_DICT["HeapOverFlow"] += 1
    elif act.globals['module'] == 'UseAfterFree':
        VULN_DICT["UseAfterFree"] += 1
        module_name = "use_after_free"
    elif act.globals['module'] == 'DoubleFree':
        VULN_DICT["DoubleFree"] += 1
        module_name = "double_free"

    ret_addr = act.callstack.ret_addr
    block=act.project.factory.block(ret_addr)
    try:
        func_addr=act.globals['func_block_addr'][block.addr]
    except:
        func_addr=act.globals['func_block_addr'][act.addr]

    # get function name
    cfg = act.globals['cfg']
    func = cfg.kb.functions[func_addr]

    process_temp = []
    # do write to report file
    do_write(f'[*]{module_name} found in function: {func.name}\n')
    do_write(f'    === Process ===\n')
    before_main = True
    for addr in act.history.bbl_addrs:
        if addr not in act.globals['_sim_procedures']:
            try:
                if cfg.kb.functions[addr].name=='main':
                    before_main = False
                
                if not before_main:
                    do_write(f'    {cfg.kb.functions[addr].name}\n')
                    process_temp.append(cfg.kb.functions[addr].name)
            except:
                pass
    do_write(f'    ===============\n\n')
    data = {
        'vuln_func': func.name,
        'process': process_temp,
    }
    VULNS[act.globals['module']].append(data)

def check_malloc(act):
    info(f'I will check malloc. in {hex(act.addr)}')

    # get first parameter address of malloc
    Arg=act.project.factory.cc().ARG_REGS[0]
    first_param=act.solver.eval(act.regs.get(Arg))
    act.globals['malloc_size']=first_param

def check_free(act):
    info(f'I will check free. in {hex(act.addr)}')

    # get first parameter address of malloc
    Arg=act.project.factory.cc().ARG_REGS[0]
    first_param=act.solver.eval(act.regs.get(Arg))

    # check if first_param in malloc_addr, if not, add it
    if first_param not in act.globals['free_malloc_addr']:
        act.globals['free_malloc_addr'].append(first_param)
    elif act.globals['module'] == 'DoubleFree':
        print("find double free")
        print_result(act)

def check_mem_write(state):
    if state.inspect.mem_write_address == None:
        return
    
    # get write address and size
    write_addr = state.solver.eval(state.inspect.mem_write_address)
    write_size = state.inspect.mem_write_length

    # check if write address in malloc_addr
    if write_addr not in list(state.globals['malloc_addr'].keys()):
        return
    
    if state.globals['module'] == 'HeapOverFlow':
        if type(write_size) != int:
            write_size = state.solver.eval(write_size)
            
        # check if write size > malloc size
        if write_size > state.globals['malloc_addr'][write_addr]:
            print("find heap overflow")
            print('write', 'from', state.inspect.mem_write_address)
            print_result(state)

    elif state.globals['module'] == 'UseAfterFree':
        if write_addr in state.globals['free_malloc_addr']:
            print("find use after free")
            print('write', 'from', state.inspect.mem_write_address)
            print_result(state)

def check_mem_read(state):
    if state.inspect.mem_read_address == None:
        return
    
    # get read address and size
    read_addr = state.solver.eval(state.inspect.mem_read_address)
    read_size = state.inspect.mem_read_length

    # check if read address in malloc_addr
    if read_addr not in list(state.globals['malloc_addr'].keys()):
        return

    if state.globals['module'] == 'HeapOverFlow':
        # sometimes read_size is BVV, so we need to convert it to int
        if type(read_size) != int:
            read_size = state.solver.eval(read_size)

        # check if read size > malloc size
        if read_size > state.globals['malloc_addr'][read_addr]:
            print("find heap overflow")
            print('read', 'from', state.inspect.mem_read_address)
            print_result(state)
    
    elif state.globals['module'] == 'UseAfterFree':
        # check if read address in free_malloc_addr
        if read_addr in state.globals['free_malloc_addr']:
            print("find use after free")
            print('read', 'from', state.inspect.mem_read_address)
            print_result(state)

def HeapVuln(proj, isHeapOverFlow=False, isUseAfterFree=False, isDoubleFree=False):
    # binary process
    initial_state = proj.factory.entry_state(
        add_options = { 
            angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY,
            angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS,
            #angr.options.CONCRETIZE_SYMBOLIC_WRITE_SIZES,
            angr.options.UNICORN,
            angr.options.FAST_REGISTERS
        }
    )

    cfg = proj.analyses.CFGFast()

    # set module name
    initial_state.globals['module'] = 'HeapOverFlow'
    if isUseAfterFree:
        initial_state.globals['module'] = 'UseAfterFree'
    elif isDoubleFree:
        initial_state.globals['module'] = 'DoubleFree'

    # if you want to use cfg in other function, you need to add this line
    initial_state.globals['cfg']=cfg

    # set global variable
    initial_state.globals['_sim_procedures']=list(proj._sim_procedures.keys())
    initial_state.globals['func_block_addr']={}
    initial_state.globals['find_malloc_flag']=False
    initial_state.globals['malloc_addr']={}
    initial_state.globals['free_malloc_addr']=[]
    initial_state.globals['malloc_size']=0

    # 使用double free的話，就不需要檢查mem_write和mem_read
    if not isDoubleFree:
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
                block_addrs = list(func.block_addrs)
                for block_addr in block_addrs:
                    block = act.project.factory.block(block_addr)
                    for insn_addr in block.instruction_addrs:
                        act.globals['func_block_addr'][insn_addr] = act.addr
            
                act.globals['find_malloc_flag'] = False
                # print(func.name)
                if func.name == 'malloc':

                    # 避免檢查simprocedures
                    block = act.project.factory.block(act.addr)
                    if block.instructions <= 2:
                        continue
                    check_malloc(act)
                    act.globals['find_malloc_flag'] = True
                elif func.name == "free":

                    # 避免檢查simprocedures
                    block = act.project.factory.block(act.addr)
                    if block.instructions > 2:
                        continue
                    check_free(act)
                    act.globals['find_malloc_flag'] = True

            except:
                pass
        simgr.step() 

def HeapOverFlow(proj):
    HeapVuln(proj, isHeapOverFlow=True)

def UseAfterFree(proj):
    HeapVuln(proj, isUseAfterFree=True)

def DoubleFree(proj):
    HeapVuln(proj, isDoubleFree=True)
    pass

if __name__=='__main__':
    choose = input('HeapVuln: \n\t1. HeapOverFlow 2. UseAfterFree 3. DoubleFree\n')
    if choose == '1':
        info('Heap Over Flow case:')
        file_path = 'sample/build/hof'
        proj = angr.Project(file_path, auto_load_libs=False)
        HeapOverFlow(proj)
    elif choose == '2':
        info('Use After Free case:')
        file_path = 'sample/build/uaf'
        proj = angr.Project(file_path, auto_load_libs=False)
        UseAfterFree(proj)
    elif choose == '3':
        info('Double Free case:')
        file_path = 'sample/build/uaf'
        proj = angr.Project(file_path, auto_load_libs=False)
        DoubleFree(proj)