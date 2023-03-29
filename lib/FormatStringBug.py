import angr

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

        simgr.step()     

if __name__=='__main__':
    file_path = 'sample/build/sof1_64bits'
    FormatStringBug(file_path)