from pwn import *
import angr
import argparse
import pyfiglet
import os
import time
import pathlib

from lib.StackOverFlow import StackOverFlow

# get argv
def get_argv():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('proj', type=str, help="binary path")
    parser.add_argument('-s', '--save', type=str, default='report/report.txt', help="report file path")
    parser.add_argument('-m', '--module', nargs='+', default=['all'], help="vuln module")
    parser.add_argument('-t', '--limit_time', type=int, default=60, help="limit time")
    return parser.parse_args()

def main(argv):
    # load binary file
    proj = angr.Project(argv.proj)
    
    # get file path
    file_path = os.path.abspath(argv.proj)
    
    # print checksec
    elf = ELF(file_path, checksec=False)
    print(elf.checksec())

    # modules
    if argv.module==['all']:
        info('find all()')
    elif argv.module==['stack_over_flow']:
        info('find StackOverFlow()')
        StackOverFlow(file_path)
    elif argv.module==['heap_over_flow']:
        info('find HeapOverFlow()')
    elif argv.module==['format_string']:
        info('find FormatStringBug()')
    else:
        info('input error')
            
    # create report file path
    pathlib.Path(argv.save).parent.mkdir(parents=True, exist_ok=True)

    # write report
    rep_file = open(argv.save, 'w+')
    rep_file.write(f'file name: {argv.proj}\n')
    rep_file.write(f'arch: {proj.arch}\n')
    rep_file.write(f'start time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')

if __name__=='__main__':
    # magic
    print(pyfiglet.figlet_format('AutoDectVuln', font = 'slant', justify='center'))
    
    # get arguments
    argv = get_argv()
    #print(argv)

    # entry points
    main(argv)
