import pathlib

from flask import Blueprint, session, send_file

reportRoute = Blueprint('reportRoute', __name__)

@reportRoute.route("/report")
def report():
    reports={}
    print(session)
    for file_name in session['binary_files']:
        reports[file_name] = session['reports'][file_name]
    return reports

@reportRoute.route("/report/<name>", methods=['GET'])
def report_file(name):
    procs_name = session['procs_name']
    name=list(procs_name[int(name)].keys())[0]
    report_path = session['reports'][name]
    report_path = pathlib.Path(report_path).resolve()
    print(report_path)
    return send_file(report_path, as_attachment=True)