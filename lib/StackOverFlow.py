import angr

def check_head(act):
    block = act.project.factory.block(act.addr)
    # print(block.pp())
    insns = block.capstone.insns
    
    # find push rbp; mov rbp, rsp
    if(len(insns)>=2):
        insns1=insns[0]
        insns2=insns[1]
        if( not (insns1.mnemonic=="push" and insns2.mnemonic=="mov") ):
            return
        op_str1 = insns1.op_str.split(", ")
        op_str2 = insns2.op_str.split(", ")
        if( not (len(op_str1)==1 and len(op_str2)==2) ):
            return
        if( not (op_str1[0]=="rbp" and op_str2[0]=="rbp" and op_str2[1]=="rsp" )):
            return
        
        print("Found head")

def check_end(act):
    block = act.project.factory.block(act.addr)
    insns = block.capstone.insns

    # find leave; ret
    if(len(insns)>=2):
        insns1=insns[-2].mnemonic
        insns2=insns[-1].mnemonic
        # print(insns1, insns2)
        if( not (insns1=="leave" and insns2=="ret") ):
            return
        print("Found end")


def StackOverFlow(file_path):
    proj = angr.Project(file_path, auto_load_libs=False)
    initial_state = proj.factory.entry_state(
        add_options = { 
            angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY,
            angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS
        }
    )

    simgr = proj.factory.simgr(initial_state)
    while simgr.active:
        for act in simgr.active:
            check_head(act)
            check_end(act)

        simgr.step()