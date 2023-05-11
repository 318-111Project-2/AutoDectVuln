import pathlib, os, json
from datetime import datetime, timedelta
from app.database.ConnectDB import ConnectDB as con

from flask import Blueprint, send_file, redirect, url_for, render_template

reportRoute = Blueprint('reportRoute', __name__)

@reportRoute.route("/reports", methods=['GET'])
def report_index():
    isnull = False
    db = con()
    query = f"select * from analyzes order by id desc"
    list_analyzes = []
    analyzes = db.select(query)
    if len(analyzes) == 0:
        isnull = True
    else:
        for analyze in analyzes:
            created = datetime.strptime(analyze['created'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
            
            list_analyzes.append({
                'id': analyze['id'],
                'created': created,
                'status': analyze['status'],
                'message': '無'if analyze['message'] == None else analyze['message'],
            })

    db.close()

    return render_template('reports/index.html', sidebar='report', isnull=isnull, analyzes=list_analyzes)

@reportRoute.route("/report/<name>", methods=['GET'])
def report_file(name):
    web_data = {}
    if os.path.isfile('web_data.json'):
        with open('web_data.json', 'r') as f:
            web_data = json.load(f)
    else:
        return redirect(url_for('home'))
    
    procs_name = web_data['analyze_status']['procs_name']
    name=list(procs_name[int(name)].keys())[0]
    report_path = web_data['analyze_status']['reports'][name]
    report_path = pathlib.Path(report_path).resolve()
    return send_file(report_path, as_attachment=True)