from pwn import *
import angr
import argparse
import pyfiglet
import os
import sys
import time

def get_argv():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('proj', type=str)
    parser.add_argument('-s', '--save', type=str)
    parser.add_argument('-m', '--module', nargs='+')
    parser.add_argument('-t', '--limit_time', type=int)
    return parser.parse_args()

def main(argv):
    # load binary file
    proj = angr.Project(argv.proj)
    os.system(f'checksec {argv.proj}')

    # modules
    if argv.module==['all']:
        info('find all()')
    elif argv.module==['stack']:
        info('find StackOverFlow()')
    elif argv.module==['heap_over_flow']:
        info('find HeapOverFlow()')
    elif argv.module==['format_string']:
        info('find FormatStringBug()')
    else:
        info('input error')
        
                
    # create file
    rep_file = open('report.txt', 'w+')
    rep_file.write(f'file name: {argv.proj}\n')
    rep_file.write(f'arch: {proj.arch}\n')
    rep_file.write(f'start time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')

if __name__=='__main__':
    # magic
    print(pyfiglet.figlet_format('3 1 8 Project - 2', font = 'slant', justify='center'))
    
    # get arguments
    argv = get_argv()
    print(argv)

    # entry points
    main(argv)