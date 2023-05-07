import os, time, pathlib, json
import filetype

from flask import Blueprint, request
from hashlib import sha256
from werkzeug.utils import secure_filename

uploadRoute = Blueprint('uploadRoute', __name__)

@uploadRoute.route("/upload", methods=['POST'])
def upload():
    web_data = {}
    if os.path.isfile('web_data.json'):
        with open('web_data.json', 'r') as f:
            web_data = json.load(f)
    else:
        return {
            'msg': 'web_data not exist!',
        }

    files = request.files.getlist('file')
    binary_files = {}
    procs_name = []
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
            procs_name.append({
                    filename: hash_filename
                })
            
    
    print(binary_files)
    web_data['analyze_status']['binary_files'] = binary_files
    web_data['analyze_status']['procs_name'] = procs_name

    with open('web_data.json', 'w') as f:
        json.dump(web_data, f)

    return {
        'msg': 'success',
        'binary_files': list(binary_files.keys())
    }