import os, json
import time
import pathlib
import multiprocessing as mp

from flask import Blueprint, request, render_template, url_for, redirect
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

@analyzeRoute.route("/analyze", methods=['GET'])
def analyze_get():
    web_data={
        'analyze_status':{
            'status': 'not start',
            'step': 0,
            'binary_files': {}, # {'filename': 'hash_filename'}
            'procs': {}, # {'hash_filename': False}
            'procs_name': [], # [{'filename': 'hash_filename'}]
            'reports': {}, # {'filename': 'report_path'}
        },
        'reports':{},
    }
    if os.path.isfile('web_data.json'):
        with open('web_data.json', 'r') as f:
            web_data = json.load(f)
    else:
        with open('web_data.json', 'w') as f:
            json.dump(web_data, f)
    web_data['analyze_status']['step'] = 0
    with open('web_data.json', 'w') as f:
        json.dump(web_data, f)

    return redirect(url_for('analyzeRoute.analyze_step1'))

@analyzeRoute.route("/analyze/step1", methods=['GET'])
def analyze_step1():
    web_data = {}
    if os.path.isfile('web_data.json'):
        with open('web_data.json', 'r') as f:
            web_data = json.load(f)
    else:
        return redirect(url_for('analyzeRoute.analyze_get'))
    if web_data['analyze_status']['step'] != 0:
        return redirect(url_for('analyzeRoute.analyze_get'))

    web_data['analyze_status']['step'] = 1
    with open('web_data.json', 'w') as f:
        json.dump(web_data, f)
    
    return render_template('analyze/step1.html', sidebar='analyze')

@analyzeRoute.route("/analyze/step2", methods=['GET'])
def analyze_step2():
    web_data = {}
    if os.path.isfile('web_data.json'):
        with open('web_data.json', 'r') as f:
            web_data = json.load(f)
    else:
        return redirect(url_for('analyzeRoute.analyze_get'))
    if web_data['analyze_status']['step'] != 1:
        return redirect(url_for('analyzeRoute.analyze_get'))
    
    web_data['analyze_status']['step'] = 2
    with open('web_data.json', 'w') as f:
        json.dump(web_data, f)
    
    return render_template('analyze/step2.html', sidebar='analyze', analyze_status=web_data['analyze_status'])


@analyzeRoute.route("/analyze", methods=['POST'])
def analyze():
    web_data = {}
    if os.path.isfile('web_data.json'):
        with open('web_data.json', 'r') as f:
            web_data = json.load(f)
    else:
        return {
            'msg': 'web_data not exist!',
        }
    
    procs = {}
    procs_name = []

    binary_files = web_data['analyze_status']['binary_files']

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
        

        web_data['analyze_status']['reports'][binary_file] = report_path
        with open('web_data.json', 'w') as f:
            json.dump(web_data, f)

        procs[hash_filename] = False

        p1.start()

    with open('web_data.json', 'w') as f:
        json.dump(web_data, f)

    return {
        'msg': 'success',
        'binary_files': list(binary_files.keys())
    }


@analyzeRoute.route("/analyze_progress")
def analyze_progress():
    web_data = {}
    if os.path.isfile('web_data.json'):
        with open('web_data.json', 'r') as f:
            web_data = json.load(f)
    else:
        return {
            'msg': 'web_data not exist!',
        }
    procs_name = web_data['analyze_status']['procs_name']

    status = []
    for name_dict in procs_name:
        name=list(name_dict.keys())[0]
        report_path = web_data['analyze_status']['reports'][name]
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
