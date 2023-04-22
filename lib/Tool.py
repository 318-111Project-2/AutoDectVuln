import os
import pathlib

REP_FILE = None
VULN_DICT = {
    'StackOverFlow': 0,
    'FormatStringBug': 0
}

def create_report_file(argv) :
    global REP_FILE
    pathlib.Path(argv.save).parent.mkdir(parents=True, exist_ok=True)
    REP_FILE = open(argv.save, 'w+')

def do_write(string: str) -> None:
    REP_FILE.write(string)

