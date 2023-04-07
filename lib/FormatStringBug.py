from pwn import *
import angr
def print_result(act):

    # get function name
    cfg = act.project.analyses.CFGFast()
    # func = cfg.kb.functions[func_addr]
    # print("format_string_bug:", func.name)

    print('=============== Process ================')
    for addr in act.history.bbl_addrs:
        try:
            print(cfg.kb.functions[addr].name)
        except:
            pass
    print('========================================')

def check_printf(act):
    info(f'I will check printf. in {hex(act.addr)}')
    
    # get first parameter address of printf
    Arg=act.project.factory.cc().ARG_REGS[0]
    first_param=act.regs.get(Arg)
    
    # 復原原本的值
    if act.globals['origin_str'].get(first_param) != None:
        origin_str=act.globals['origin_str'][first_param]
        act.memory.store(first_param, origin_str)

    # check first parameter symbolic
    first_param_stack=act.memory.load(first_param, 8, endness=angr.archinfo.Endness.LE)
    if first_param_stack.symbolic:
        
        # 將原本的值存起來
        act.globals['origin_str'][first_param] = first_param_stack

        # 假如first_param symbolic，則將其值設為0，以免程式crash
        temp_str='0x'+str(0)*64
        act.memory.store(first_param, temp_str, endness=angr.archinfo.Endness.LE)
        first_param_stack=act.memory.load(first_param, 8, endness=angr.archinfo.Endness.LE)
        print("first_param symbolic")
        print_result(act)
        return

def FormatStringBug(file_path):
    # binary process
    proj = angr.Project(file_path, auto_load_libs=False)
    initial_state = proj.factory.entry_state(
        add_options = { 
            angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY,
            angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS
        }
    )
    initial_state.globals['origin_str']={}
    
     # main exlpore
    simgr = proj.factory.simgr(initial_state)
    while simgr.active:
        for act in simgr.active:
            '''
                check firest parameter of "printf" 
            '''
            try:
                # print(act.addr)
                cfg = act.project.analyses.CFGFast()
                func = cfg.kb.functions[act.addr]

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
    file_path = 'sample/build/fmt'
    FormatStringBug(file_path)