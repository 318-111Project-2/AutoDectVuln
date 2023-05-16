import os, shutil, time, pathlib
import multiprocessing as mp
from app.database.ConnectDB import ConnectDB as con

from flask import Blueprint, request, render_template, url_for, redirect
import sys 
sys.path.append("../..") 
from main import main as main_analyze

analyzeRoute = Blueprint('analyzeRoute', __name__)

def job(hash_name, file_name, module, file_id):
    binary_file = f'uploads/{hash_name}'
    report_path = f'report/report_{file_name}_{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}.txt'
    WEB_Data = {
        'proj': pathlib.Path(f'uploads/{hash_name}').resolve(),
        'save': pathlib.Path(report_path).resolve(),
        'module': [module],
        'limit_time': 60,
        'file_id': file_id
    }
    analyze_results, total_time, vulns = main_analyze(WEB_Data=WEB_Data)
    
    os.remove(binary_file)

    db = con()
    query = f"select * from files where id = {file_id}"
    file = db.select(query)[0]
    results_id = file['results_id']
    query = f"select * from results where id = {results_id}"
    result = db.select(query)[0]
    query = "update results set run_time = ? where id = ?"
    data = (total_time, results_id)
    db.update(query, data)
    for key, value in analyze_results.items():
        if value != 0:
            vulns_id = db.insert('vulns', ['results_id', 'vuln_name', 'vuln_num'], (results_id, key, value))
            datas = vulns[key]
            for data in datas:
                vuln_func = data['vuln_func']
                process = ' -> '.join(data['process'])
                db.insert('process', ['vulns_id', 'vuln_func', 'process'], (vulns_id, vuln_func, process))

    db.close()

@analyzeRoute.route("/analyze", methods=['GET'])
def analyze_get():
    if os.path.exists('report'):
        shutil.rmtree('report')

    db = con()
    query = f"select * from analyzes order by id desc limit 1"
    analyze = db.select(query)
    if len(analyze) != 0:
        analyze = analyze[0]
        if analyze['status'] == 'pending' or analyze['status'] == 'running':
            db.close()
            return redirect(url_for('analyzeRoute.analyze_step2'))
    
    return redirect(url_for('analyzeRoute.analyze_step1'))

@analyzeRoute.route("/analyze/step1", methods=['GET'])
def analyze_step1():
    db = con()
    query = f"select * from analyzes order by id desc limit 1"
    analyze = db.select(query)
    if len(analyze) != 0:
        analyze = analyze[0]
        if analyze['status'] == 'pending' or analyze['status'] == 'running':
            db.close()
            return redirect(url_for('analyzeRoute.analyze_step2'))
    
    return render_template('analyze/step1.html', sidebar='analyze')

@analyzeRoute.route("/analyze/step2", methods=['GET'])
def analyze_step2():
    db = con()
    query = f"select * from analyzes order by id desc limit 1"
    analyze = db.select(query)
    if len(analyze) == 0:
        return redirect(url_for('home'))
    analyze = analyze[0]

    if analyze['status'] == 'finished':
        db.close()
        return redirect(url_for('analyzeRoute.analyze_get'))

    isRunning = False
    if analyze['status'] == 'running':
        isRunning = True
    
    analyze_id = analyze['id']
    analyze_name = analyze['name']

    query = f"select * from files where analyze_id = {analyze_id}"
    files = db.select(query)
    files_dict = []
    for file in files:
        module = ''
        if isRunning:
            query = f"select * from results where id = {file['results_id']}"
            result = db.select(query)[0]
            module = result['module']
        files_dict.append({
            'id': file['id'],
            'file_name': file['file_name'],
            'module': module,
        }) 

    db.close()
    
    return render_template('analyze/step2.html', sidebar='analyze', files=files_dict, isRunning=isRunning, analyze_name=analyze_name)


@analyzeRoute.route("/analyze", methods=['POST'])
def analyze():
    db = con()
    query = f"select * from analyzes order by id desc limit 1"
    analyze = db.select(query)
    if len(analyze) == 0:
        return redirect(url_for('home'))
    analyze_id = analyze[0]['id']

    query = f"select * from files where analyze_id = {analyze_id}"
    files = db.select(query)

    modules = request.get_json()
    query = "update analyzes set status = ? where id = ?"
    data = ('running', analyze_id)
    db.update(query, data)

    for file in files:
        file_id = file['id']
        module = modules[str(file['id'])]
        file_name = file['file_name']
        hash_name = file['hash_name']
        file_path = os.path.join('uploads', hash_name)
        if not (os.path.isfile(file_path)):
            query = "update analyzes set status = ? , message = ? where id = ?"
            data = ('error', 'file not exist!', analyze_id)
            db.update(query, data)
            print('file not exist!')
            return {
                'msg': 'file not exist!',
            }

        report_path = f'report/report_{file_name}_{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}.txt'
        p1 = mp.Process(target=job, args=(
            hash_name, file_name, module, file_id))
        
        results_id = db.insert('results', ['analyze_id', 'module'], (analyze_id, module))

        query = "update files set results_id = ? where id = ?"
        data = (results_id, file['id'])
        db.update(query, data)

        p1.start()

    db.close()

    return {
        'msg': 'success',
    }


@analyzeRoute.route("/analyze_process")
def analyze_process():
    db = con()
    query = f"select * from analyzes order by id desc limit 1"
    analyze = db.select(query)
    if len(analyze) == 0:
        return redirect(url_for('home'))
    analyze_id = analyze[0]['id']

    status = {}
    AllFinished = True

    files = db.select(f"select * from files where analyze_id = {analyze_id}")
    for file in files:
        result_id = file['results_id']
        results = db.select(f"select * from results where id = {result_id} and run_time is not null")
        if len(results) == 0:
            AllFinished = False
            status[file['id']] = 'running'
        else:
            status[file['id']] = 'finished'

    if AllFinished:
        query = "update analyzes set status = ? where id = ?"
        data = ('finished', analyze_id)
        db.update(query, data)

    db.close()
    return {
        'msg': 'success',
        'process': status,
        'analyze_id': analyze_id,
    }

@analyzeRoute.route("/cancel_analyze", methods=['POST'])
def cancel_analyze():
    db = con()
    query = f"select * from analyzes order by id desc limit 1"
    analyze = db.select(query)[0]
    analyze_id = analyze['id']
    query = f"update analyzes set status = ? where id = ?"
    data = ('canceled', analyze_id)
    db.update(query, data)
    db.close()
    return {
        'msg': 'success',
    }