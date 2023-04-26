import os
import time
import pathlib
import multiprocessing as mp

from flask import Blueprint, request, session
import sys 
sys.path.append("../..") 
from main import main as main_analyze

analyzeRoute = Blueprint('analyzeRoute', __name__)

def job(file_path, file_name, module):
    binary_file = f'uploads/{file_path}'
    report_path = f'report/report_{file_name}_{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}.txt'
    WEB_Data = {
        'proj': pathlib.Path(f'uploads/{file_path}').resolve(),
        'save': pathlib.Path(report_path).resolve(),
        'module': [module],
        'limit_time': 60
    }
    main_analyze(WEB_Data=WEB_Data)
    os.remove(binary_file)


@analyzeRoute.route("/analyze", methods=['POST'])
def analyze():
    procs = {}
    procs_name = []

    binary_files = session['binary_files']

    modules = request.get_json()

    for binary_file in binary_files:
        hash_filename = binary_files[binary_file]
        file_path = os.path.join('uploads', hash_filename)
        if not (os.path.isfile(file_path)):
            print('file not exist!')
            return {
                'msg': 'file not exist!',
            }

        report_path = f'report/report_{binary_file}_{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}.txt'
        p1 = mp.Process(target=job, args=(
            binary_files[binary_file], binary_file, modules[binary_file]))
        
        session['reports'][binary_file] = report_path

        procs[hash_filename] = False
        procs_name.append({
                binary_file: hash_filename
            })

        p1.start()

    session['procs_name'] = procs_name

    return {
        'msg': 'success',
        'binary_files': list(binary_files.keys())
    }


@analyzeRoute.route("/analyze_progress")
def analyze_progress():
    procs_name = session['procs_name']

    status = []
    for name_dict in procs_name:
        name=list(name_dict.keys())[0]
        report_path = session['reports'][name]
        report_path = pathlib.Path(report_path).resolve()
        if not report_path.exists():
            status.append('running')
            continue
        file_stats = os.stat(report_path)
        if file_stats.st_size == 0:
            status.append('running')
            continue
        status.append('finished')
    return {
        'msg': 'success',
        'progress': status
    }
