import os, time, pathlib, shutil
import filetype

from flask import Blueprint, request
from hashlib import sha256
from werkzeug.utils import secure_filename
from app.database.ConnectDB import ConnectDB as con

uploadRoute = Blueprint('uploadRoute', __name__)

@uploadRoute.route("/upload", methods=['POST'])
def upload():
    if not os.path.exists('uploads'):
        os.mkdir('uploads')
    else:
        shutil.rmtree('uploads')
    db = con()
    analyze_id = db.insert('analyzes', ['status'], ('pending',))

    files = request.files.getlist('file')
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            hash_filename = sha256(f'{filename}{time.time()}'.encode()).hexdigest()
            file_path=os.path.join('uploads', hash_filename)
            pathlib.Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            file.save(file_path)
            
            kind = filetype.guess(file_path)
            if kind is None:
                query = 'UPDATE analyzes SET status = ? , message = ? WHERE id = ?'
                data = ('not executable file!', 'error', analyze_id)
                db.update(query, data)
                print('Cannot guess file type!')
                os.remove(file_path)
                return {
                    'msg': 'not executable file!',
                }
            
            if not(kind.extension == 'elf' and kind.mime == 'application/x-executable'):
                query = 'UPDATE analyzes SET status = ? , message = ? WHERE id = ?'
                data = ('not executable file!', 'error', analyze_id)
                db.update(query, data)
                print('not executable file!')
                os.remove(file_path)
                return {
                    'msg': 'not executable file!',
                }
            

            db.insert('files', ['analyze_id', 'file_name', 'hash_name'], (analyze_id, filename, hash_filename))

    db.close()

    return {
        'msg': 'success',
    }