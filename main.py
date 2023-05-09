from pwn import *
import angr
import argparse
import pyfiglet
import os
import time
import pathlib

from lib.StackOverFlow import StackOverFlow
from lib.FormatStringBug import FormatStringBug
from lib.HeapVuln import HeapOverFlow, UseAfterFree, DoubleFree
from lib.Tool import *

'''
    get argv

    usage: main.py [-h] [-s SAVE] [-m MODULE [MODULE ...]] [-t LIMIT_TIME] proj
    main.py: error: the following arguments are required: proj
'''
def get_argv() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('proj', type=str, help="binary path")
    parser.add_argument('-s', '--save', type=str, default='report/report.txt', help="report file path")
    parser.add_argument('-m', '--module', nargs='+', default=['all'], help="vuln module")
    parser.add_argument('-t', '--limit_time', type=int, default=60, help="limit time")
    return parser.parse_args()


'''
    load the binary file
'''
def load(file_path: str) -> angr.project.Project:
    proj = angr.Project(file_path, auto_load_libs=False)
    #proj = angr.Project(file_path, auto_load_lib=True)
    return proj

'''
    write to report file
'''
def write_to_report(argv, proj, action) -> None:
    '''format
        File path:
        Architecture:
        Start Time:
        =========== Vulnerability Detection =========
        
        ...
        
        [*]StackOverFlow: {VULN_DICT["StackOverFlow"]
        [*]FormatStringBug: {VULN_DICT["FormatStringBug"]
        [*]HeapOverFlow: {VULN_DICT["HeapOverFlow"]
        [*]UseAfterFree: {VULN_DICT["UseAfterFree"]
        [*]DoubleFree: {VULN_DICT["DoubleFree"]
    '''
    if action=='init':
        do_write(f'File path: {argv.proj}\n')
        do_write(f'Architecture: {str(proj.arch)[1:-1]}\n')
        do_write(f'Start Time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}\n\n')
        do_write(f'=========== Vulnerability Detection =========\n\n')
    
    elif action=='finish':
        do_write(f'[*]StackOverFlow: {VULN_DICT["StackOverFlow"]}\n')
        do_write(f'[*]FormatStringBug: {VULN_DICT["FormatStringBug"]}\n')
        do_write(f'[*]HeapOverFlow: {VULN_DICT["HeapOverFlow"]}\n')
        do_write(f'[*]UseAfterFree: {VULN_DICT["UseAfterFree"]}\n')
        do_write(f'[*]DoubleFree: {VULN_DICT["DoubleFree"]}\n')


'''
    Web Control
'''
class Web_Control:
    def __init__(self, proj, save, module, limit_time):
        self.proj = proj
        self.save = save
        self.module = module
        self.limit_time = limit_time

# main function
def main(argv: argparse.Namespace=None, WEB_Data=False) -> None:

    # ================================== initialize =========================================
    if WEB_Data:
        argv=Web_Control(WEB_Data['proj'], WEB_Data['save'], WEB_Data['module'], WEB_Data['limit_time'])
        
    # binary load 
    proj = load(argv.proj)

    # print checksec
    elf = ELF(argv.proj, checksec=False)
    print(elf.checksec())
    # =======================================================================================

    
    # ==================================== write report =====================================
    #create report file path
    create_report_file(argv)
    write_to_report(argv, proj, 'init')

    # =======================================================================================

    Start_time = time.time()
    # ====================================== modules ========================================
    if argv.module==['all']:
        info('find all()')
        StackOverFlow(proj)
        FormatStringBug(proj)
        HeapOverFlow(proj)
        UseAfterFree(proj)
        DoubleFree(proj)

    elif argv.module==['stack_over_flow']:
        info('find StackOverFlow()')
        StackOverFlow(proj)
    
    elif argv.module==['format_string_bug']:
        info('find FormatStringBug()')
        FormatStringBug(proj)
    elif argv.module==['heap_over_flow']:
        info('find HeapOverFlow()')
        HeapOverFlow(proj)

    elif argv.module==['use_after_free']:
        info('find UseAfterFree()')
        UseAfterFree(proj)

    elif argv.module==['double_free']:
        info('find DoubleFree()')
        DoubleFree(proj)
    
    else:
        info('input error')

    # ======================================================================================            
    End_time = time.time()
    do_write(f'[*]Time: {round(End_time-Start_time, 2)} seconds.\n')
    print(f'[*]Time: {round(End_time-Start_time, 2)} seconds')

    # ==================================== finish ==========================================
    write_to_report(argv, proj, 'finish')
    close_report_file()
    # ======================================================================================            
    return VULN_DICT

if __name__=='__main__':
    # magic
    print(pyfiglet.figlet_format('AutoDectVuln', font = 'slant', justify='center'))
    
    # get arguments
    argv = get_argv()
    #print(argv)

    # entry points
    main(argv)
