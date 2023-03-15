import angr

def print_result(act):
    print("stdin:", act.posix.dumps(0))
    print("stdout:", act.posix.dumps(1))

def check_head(act):
    block = act.project.factory.block(act.addr)
    insns = block.capstone.insns
    
    # find push rbp; mov rbp, rsp
    if( not (len(insns)>=2)):
        return
    
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
    
    # 取得function 的return address
    ret_addr = act.callstack.ret_addr
    rbp=act.regs.rbp

    # 儲存function 的 rbp, key 為 return address
    act.globals['rbp_list'][ret_addr]=rbp
    
    # print("Found head")

def check_end(act):
    block = act.project.factory.block(act.addr)
    insns = block.capstone.insns

    # find leave; ret
    if( not (len(insns)>=2)):
        return
    
    insns1=insns[-2].mnemonic
    insns2=insns[-1].mnemonic
    # print(insns1, insns2)
    if( not (insns1=="leave" and insns2=="ret") ):
        return
    # print("Found end")
    
    rbp=act.regs.rbp
    rbp_stack = act.memory.load(rbp, 8, endness=angr.archinfo.Endness.LE)
    ret_addr=act.callstack.ret_addr
    origin_rbp=act.globals['rbp_list'][ret_addr]
    
    # check rbp symbolic
    if(rbp_stack.symbolic):
        act.memory.store(rbp, origin_rbp)
        
        print("rbp symbolic")
        print_result(act)

    # check return address symbolic
    ret_stack=act.memory.load(rbp+8, 8, endness=angr.archinfo.Endness.LE)
    if(ret_stack.symbolic):
        origin_ret_addr=act.solver.BVV(act.callstack.ret_addr, 64)
        act.memory.store(rbp+8, origin_ret_addr, endness=angr.archinfo.Endness.LE)

        print("ret symbolic")
        print_result(act)
        

def StackOverFlow(file_path):
    proj = angr.Project(file_path, auto_load_libs=False)
    initial_state = proj.factory.entry_state(
        add_options = { 
            angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY,
            angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS
        }
    )
    
    # 儲存rbp
    initial_state.globals['rbp_list']={}

    simgr = proj.factory.simgr(initial_state)
    while simgr.active:
        for act in simgr.active:
            check_head(act)
            check_end(act)

        simgr.step()