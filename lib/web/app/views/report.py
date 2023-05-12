import pathlib, os, json
from datetime import datetime, timedelta
from app.database.ConnectDB import ConnectDB as con

from flask import Blueprint, render_template

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

@reportRoute.route("/reports/<analyze_id>", methods=['GET'])
def report_detail(analyze_id):
    db = con()
    query = f"select an.created, f.file_name, r.module, r.run_time, r.progress, v.vuln_name, v.vuln_num from ((analyzes as an inner join files as f on an.id = f.analyze_id) inner join results as r on r.id = f.results_id) left join vulns as v on v.results_id = r.id where an.id = {analyze_id}"
    datas = db.select(query)
    print(len(datas))
    analyze_datas = []
    for data in datas:
        analyze_datas.append({
            'created': datetime.strptime(data['created'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=8),
            'file_name': data['file_name'],
            'module': data['module'],
            'run_time': data['run_time'],
            'progress': data['progress'],
            'vuln_name': data['vuln_name'],
            'vuln_num': data['vuln_num'],
        })
        # print(data['created'], data['file_name'], data['module'], data['run_time'], data['progress'], data['vuln_name'], data['vuln_num'])

    return render_template('reports/detail.html', sidebar='report', analyze_datas=analyze_datas)