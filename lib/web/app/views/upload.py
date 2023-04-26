import os, time, pathlib
import filetype

from flask import Blueprint, flash, request, redirect, url_for, render_template, jsonify, session
from flask import current_app
from flask import abort
from hashlib import sha256
from flask_session import Session
from werkzeug.utils import secure_filename

uploadRoute = Blueprint('uploadRoute', __name__)

@uploadRoute.route("/upload", methods=['POST'])
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