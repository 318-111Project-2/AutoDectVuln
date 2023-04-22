import os
import pathlib

def create_report_file(argv) :
    pathlib.Path(argv.save).parent.mkdir(parents=True, exist_ok=True)
    global rep_file
    rep_file = open(argv.save, 'w+')
    return rep_file 

def do_write(string: str) -> None:
    rep_file.write(string)

