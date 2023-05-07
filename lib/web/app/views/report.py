import pathlib, os, json

from flask import Blueprint, send_file, redirect, url_for

reportRoute = Blueprint('reportRoute', __name__)

# @reportRoute.route("/report")
# def report():
#     web_data = {}
#     if os.path.isfile('web_data.json'):
#         with open('web_data.json', 'r') as f:
#             web_data = json.load(f)
#     else:
#         return redirect(url_for('home'))
#     reports={}
#     print(session)
#     for file_name in session['binary_files']:
#         reports[file_name] = session['reports'][file_name]
#     return reports

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