from pwn import *
import angr
from lib.Tool import *

def print_result(act: angr.sim_state.SimState) -> None:
    ret_addr = act.callstack.ret_addr
    block=act.project.factory.block(ret_addr)
    func_addr=act.globals['func_block_addr'][block.addr]

    # get function name
    cfg = act.project.analyses.CFGFast()
    func = cfg.kb.functions[func_addr]
    
    '''debug
    print("format_string_bug:", func.name)
    print('=============== Process ================')
    for addr in act.history.bbl_addrs:
        try:
            print(cfg.kb.functions[addr].name)
        except:
            pass
    print('========================================')
    '''

    # do write to report file
    do_write(f'[*]format_string_bug found in function: {func.name}\n')
    do_write(f'    === Process ===\n')
    for addr in act.history.bbl_addrs:
        try:
            do_write(f'    {cfg.kb.functions[addr].name}\n')
        except:
            pass
    do_write(f'    ===============\n\n')
   
def check_printf(act: angr.sim_state.SimState) -> None:
    info(f'I will check printf. in {hex(act.addr)}')
    
    # get first parameter address of printf
    Arg=act.project.factory.cc().ARG_REGS[0]
    first_param=act.regs.get(Arg)
    
    # recover original value
    if act.globals['origin_str'].get(first_param) != None:
        origin_str=act.globals['origin_str'][first_param]
        act.memory.store(first_param, origin_str)

    # check first parameter symbolic
    first_param_stack=act.memory.load(first_param, 8, endness=angr.archinfo.Endness.LE)
    if first_param_stack.symbolic:
        
        # store origin value
        act.globals['origin_str'][first_param] = first_param_stack

        # if first_param symbolic，then set the value=0 to avoid the program crash
        temp_str='0x'+str(0)*64
        act.memory.store(first_param, temp_str, endness=angr.archinfo.Endness.LE)
        first_param_stack=act.memory.load(first_param, 8, endness=angr.archinfo.Endness.LE)
        #print("first_param symbolic")
        print_result(act)
        return

def FormatStringBug(proj: angr.project.Project) -> None:
    # binary process
    initial_state = proj.factory.entry_state(
        add_options = { 
            angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY,
            angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS
        }
    )
    initial_state.globals['origin_str']={}
    initial_state.globals['func_block_addr']={}
    
     # main exlpore
    simgr = proj.factory.simgr(initial_state)
    while simgr.active:
        for act in simgr.active:
            '''
                check first parameter of "printf" 
            '''
            try:
                # print(act.addr)
                cfg = act.project.analyses.CFGFast()
                func = cfg.kb.functions[act.addr]

                # get function block address
                block_addrs=list(func.block_addrs)
                for block_addr in block_addrs:
                    act.globals['func_block_addr'][block_addr]=act.addr

                # print(func.name)
                if func.name == 'printf':

                    # 避免檢查simprocedures
                    block = act.project.factory.block(act.addr)
                    if block.instructions >2:
                        continue
                    check_printf(act)
            except:
                pass
        simgr.step()     

if __name__=='__main__':
    info(f'Format String Bug case:')  
    file_path = 'sample/build/fmt'
    proj = angr.Project(file_path, auto_load_libs=False)
    FormatStringBug(proj)

    print('\n')

    info(f'No Format String Bug case:')
    file_path = 'sample/build/no_fmt'
    proj = angr.Project(file_path, auto_load_libs=False)
    FormatStringBug(proj)
