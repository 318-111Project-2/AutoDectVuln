import os, time, pathlib, json
from hashlib import sha256
from flask import Flask, redirect, render_template, request, url_for, session, send_file
from flask_session import Session
from werkzeug.utils import secure_filename
import filetype
import multiprocessing as mp
import sys 
sys.path.append("../..") 
from main import main as main_analyze

app = Flask(__name__)
app.config.from_pyfile('config.py')
Session(app)


@app.route("/")
def home():
    session['binary_files'] = {}
    session['reports']={}
    return render_template('home.html')

@app.route("/upload", methods=['POST'])
def upload():
    
    files = request.files.getlist('file')
    binary_files = {}
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            hash_filename = sha256(f'{filename}{time.time()}'.encode()).hexdigest()
            file_path=os.path.join('uploads', hash_filename)
            pathlib.Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            file.save(file_path)
            
            kind = filetype.guess(file_path)
            if kind is None:
                print('Cannot guess file type!')
                os.remove(file_path)
                return {
                    'msg': 'not executable file!',
                }
            
            if not(kind.extension == 'elf' and kind.mime == 'application/x-executable'):
                print('not executable file!')
                os.remove(file_path)
                return {
                    'msg': 'not executable file!',
                }
            
            binary_files[filename] = hash_filename
            
    
    print(binary_files)
    session['binary_files']=binary_files

    return {
        'msg': 'success',
        'binary_files': list(binary_files.keys())
    }

def job(file_path, file_name, module):
    binary_file = f'uploads/{file_path}'
    report_path = f'report/report_{file_name}_{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}.txt'
    WEB_Data={
        'proj': pathlib.Path(f'uploads/{file_path}').resolve(),
        'save': pathlib.Path(report_path).resolve(),
        'module': [module],
        'limit_time': 60
    }
    main_analyze(WEB_Data=WEB_Data)
    os.remove(binary_file)

procs = []
procs_name=[]

@app.route("/analyze", methods=['POST'])
def analyze():
    global procs, procs_name
    procs = []
    procs_name=[]
    binary_files=session['binary_files']
    
    modules = request.get_json()
    
    for binary_file in binary_files:
        hash_filename=binary_files[binary_file]
        file_path=os.path.join('uploads', hash_filename)
        if not(os.path.isfile(file_path)):
            print('file not exist!')
            return {
                'msg': 'file not exist!',
            }
        
        report_path = f'report/report_{binary_file}_{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}.txt'
        p1 = mp.Process(target=job,args=(binary_files[binary_file], binary_file, modules[binary_file]))
        session['reports'][binary_file] = report_path
        procs.append(p1)
        procs_name.append(binary_file)
        print(procs_name)

        p1.start()
        
    return {
        'msg': 'success',
        'binary_files': list(binary_files.keys())
    }

@app.route("/analyze_progress")
def analyze_progress():
    global procs
    status = []
    for p in procs:
        p.join(timeout=0)
        if p.is_alive():
            status.append('running')
        else:
            status.append('finished')
    return {
        'msg': 'success',
        'progress': status
    }

@app.route("/report")
def report():
    reports={}
    print(session)
    for file_name in session['binary_files']:
        reports[file_name] = session['reports'][file_name]
    return reports

@app.route("/report/<name>", methods=['GET'])
def report_file(name):
    global procs_name
    name=procs_name[int(name)]
    report_path = session['reports'][name]
    report_path = pathlib.Path(report_path).resolve()
    print(report_path)
    return send_file(report_path, as_attachment=True)

app.run(use_reloader=False)