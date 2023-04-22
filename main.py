from pwn import *
import angr
import argparse
import pyfiglet
import os
import time
import pathlib

from lib.StackOverFlow import StackOverFlow
from lib.FormatStringBug import FormatStringBug
from lib.Tool import *

# get argv
def get_argv() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('proj', type=str, help="binary path")
    parser.add_argument('-s', '--save', type=str, default='report/report.txt', help="report file path")
    parser.add_argument('-m', '--module', nargs='+', default=['all'], help="vuln module")
    parser.add_argument('-t', '--limit_time', type=int, default=60, help="limit time")
    return parser.parse_args()


def load(file_path: str) -> angr.project.Project:
    # load binary file
    proj = angr.Project(argv.proj, auto_load_libs=False)
    return proj

# main function
def main(argv: argparse.Namespace) -> None:

    # binary load 
    proj = load(argv.proj)

    # print checksec
    elf = ELF(argv.proj, checksec=False)
    print(elf.checksec())

    
    # ==================================== write report =====================================
    #create report file path
    create_report_file(argv)
    do_write(f'File path: {argv.proj}\n')
    do_write(f'Architecture: {proj.arch}\n')
    do_write(f'Start Time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}\n\n')
    do_write(f'=========== Vulnerability Detection =========:\n\n')
    # =======================================================================================


    # modules
    if argv.module==['all']:
        info('find all()')
        StackOverFlow(proj)
        FormatStringBug(proj)
        do_write(f'[*]StackOverFlow: {VULN_DICT["StackOverFlow"]}\n')
        do_write(f'[*]FormatStringBug: {VULN_DICT["FormatStringBug"]}\n')

    elif argv.module==['stack_over_flow']:
        info('find StackOverFlow()')
        StackOverFlow(proj)
        do_write(f'[*]StackOverFlow: {VULN_DICT["StackOverFlow"]}\n')

    
    elif argv.module==['format_string_bug']:
        info('find FormatStringBug()')
        FormatStringBug(proj)
        do_write(f'[*]FormatStringBug: {VULN_DICT["FormatStringBug"]}\n')

    
    else:
        info('input error')
            
    

if __name__=='__main__':
    # magic
    print(pyfiglet.figlet_format('AutoDectVuln', font = 'slant', justify='center'))
    
    # get arguments
    argv = get_argv()
    #print(argv)

    # entry points
    main(argv)
