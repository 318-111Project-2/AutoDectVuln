import os
import pathlib

VULN_DICT = {
    'StackOverFlow': 0,
    'FormatStringBug': 0,
    'HeapOverFlow': 0,
    'UseAfterFree': 0,
    'DoubleFree': 0,
}

def create_report_file(argv) :
    global REP_FILE
    pathlib.Path(argv.save).parent.mkdir(parents=True, exist_ok=True)
    REP_FILE = open(argv.save, 'w+')

def do_write(string: str) -> None:
    REP_FILE.write(string)

def close_report_file():
    REP_FILE.close()
