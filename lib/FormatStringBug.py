from pwn import *
import angr

def check_printf(act):
    info(f'I will check printf. in {hex(act.addr)}')

def FormatStringBug(file_path):
    # binary process
    proj = angr.Project(file_path, auto_load_libs=False)
    initial_state = proj.factory.entry_state(
        add_options = { 
            angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY,
            angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS
        }
    )
    
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
                    check_printf(act)
            except:
                pass
        simgr.step()     

if __name__=='__main__':
    file_path = 'sample/build/fmt'
    FormatStringBug(file_path)