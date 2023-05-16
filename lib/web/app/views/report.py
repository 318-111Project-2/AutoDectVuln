import pathlib, zipfile, re, glob, os, shutil
from datetime import datetime, timedelta
from app.database.ConnectDB import ConnectDB as con

from flask import Blueprint, render_template, send_file

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
            query = f"select * from files where analyze_id = {analyze['id']}"
            files = db.select(query)
            files_name = ''
            for file in files:
                files_name = files_name + file['file_name']
                if file != files[-1]:
                    files_name = files_name + ', '
                if len(files_name) > 8:
                    files_name = files_name[:8] + '...'
                    break

            analyze_name = analyze['name']
            if len(analyze_name) > 10:
                analyze_name = analyze_name[:10] + '...'

            created = datetime.strptime(analyze['created'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
            created = created.strftime('%Y-%m-%d %H:%M')
            list_analyzes.append({
                'id': analyze['id'],
                'name': analyze_name,
                'created': created,
                'files_name': files_name,
                'status': analyze['status'],
                'message': '無' if analyze['message'] == None else analyze['message'],
            })

    db.close()

    return render_template('reports/index.html', sidebar='report', isnull=isnull, analyzes=list_analyzes)

@reportRoute.route("/reports/<analyze_id>", methods=['GET'])
def report_detail(analyze_id, isDownload=False):
    db = con()
    query = f"select an.name, an.created, f.file_name, r.module, r.run_time, v.vuln_name, v.vuln_num, v.id as vuln_id from ((analyzes as an inner join files as f on an.id = f.analyze_id) inner join results as r on r.id = f.results_id) left join vulns as v on v.results_id = r.id where an.id = {analyze_id} and an.status = 'finished'"
    datas = db.select(query)
    if len(datas) == 0:
        return {'msg': 'not found'}
    
    vulns_categorys = {}

    analyze_name = datas[0]['name']
    analyze_datas = []
    analyze_created = datas[0]['created']
    i=0
    vuln_func = ''
    process_data = ''
    for data in datas:
        if data['vuln_name'] not in vulns_categorys and data['vuln_name'] != None:
            vulns_categorys[data['vuln_name']] = 0
        elif '無' not in vulns_categorys and data['vuln_name'] == None:
            vulns_categorys['無'] = 0
        if data['vuln_name'] != None:
            vulns_categorys[data['vuln_name']] += int(data['vuln_num'])
        else:
            vulns_categorys['無'] += 1
        if data['vuln_name'] != None:
            query = f"select * from process where vulns_id = {data['vuln_id']}"
            process = db.select(query)

            vuln_func = ''
            process_data = ''
            for temp in process:
                vuln_func = vuln_func + temp['vuln_func']
                process_data = process_data + temp['process']
                if temp != process[-1]:
                    vuln_func = vuln_func + '='
                    process_data = process_data + '='


        analyze_datas.append({
            'id': i,
            'created': datetime.strptime(data['created'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=8),
            'file_name': data['file_name'],
            'module': data['module'],
            'run_time': data['run_time'],
            'process': process_data if process_data != '' else '無',
            'vuln_name': data['vuln_name'] if data['vuln_name'] != None else '無',
            'vuln_num': data['vuln_num'] if data['vuln_num'] != None else '0',
            'vuln_func': vuln_func if vuln_func != '' else '無',
        })
        i=i+1
    
    isAllNone = False
    if len(vulns_categorys) == 1 and list(vulns_categorys.keys())[0] == '無':
        isAllNone = True

    db.close()

    if isDownload:
        html = render_template('reports/detail.html', 
                            sidebar='report', 
                            analyze_datas=analyze_datas,
                            analyze_created=analyze_created,
                            vulns_categorys=vulns_categorys,
                            isDownload=isDownload,
                            isAllNone=isAllNone,
                            analyze_name=analyze_name)
        
        html = re.sub(r'<script src="/', '<script src="', html)
        html = re.sub(r'<link href="/', '<link href="', html)
        
        file_name = f"分析結果-{analyze_created}"
        
        pathlib.Path(f'temp/{file_name}.html').parent.mkdir(parents=True, exist_ok=True)
        with open(f'temp/{file_name}.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        file_list = glob.glob("app/static/**", recursive=True)
        file_list.append(f'temp/{file_name}.html')
        
        with zipfile.ZipFile(f'temp/{file_name}.zip', mode='w') as zf:
            for file in file_list:
                if file.split('.')[-1] == 'html':
                    zf.write(file, file.split('temp/')[-1])
                else:
                    zf.write(file, file.split('app/static/')[-1])
        
        open_file = open(f'temp/{file_name}.zip', 'rb')

        if os.path.exists('temp'):
            shutil.rmtree('temp')

        return send_file(open_file,
                        download_name=f"分析結果-{analyze_created}.zip",
                        as_attachment=True,
                        mimetype='application/zip')

    else:
        return render_template('reports/detail.html', 
                            sidebar='report', 
                            analyze_id=analyze_id,
                            analyze_datas=analyze_datas,
                            analyze_created=analyze_created,
                            vulns_categorys=vulns_categorys,
                            isDownload=isDownload,
                            isAllNone=isAllNone,
                            analyze_name=analyze_name)

@reportRoute.route("/reports/<analyze_id>/download", methods=['GET'])
def report_download(analyze_id):
    return report_detail(analyze_id, isDownload=True)
