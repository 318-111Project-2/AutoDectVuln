import logging
import os, json

from flask import Flask, render_template, redirect
from app.configs.config import config
from app.views.analyze import analyzeRoute
from app.views.report import reportRoute
from app.views.upload import uploadRoute

dirname = os.path.dirname(__file__)

def initialize_logging(app):
    # Check if the log directory exists, if not, create it
    log_dir = app.config['LOG_DIR']
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # Define log file names
    app_log_filename = app.config['LOG_FILENAME']
    log_filenames = [app_log_filename]

    # Create empty log files if they don't exist
    for log_filename in log_filenames:
        path = os.path.join(log_dir, log_filename)
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                pass

    # Set the log level for 'selenium' and 'werkzeug' to a higher level than your application logging
    # logging.getLogger('werkzeug').setLevel(logging.WARNING)

    # Configure logging with the log file path, log level, and log format specified in the app config
    logging.basicConfig(filename=os.path.join(log_dir, app_log_filename),
                        level=app.config['LOG_LEVEL'],
                        format=app.config['LOG_FORMAT'])

def create_app(config_name):
    app = Flask(__name__,
                static_folder='static',
                static_url_path='',
                template_folder='templates',
                instance_relative_config=True)

    # Load config
    app.config.from_object(config[config_name])

    # Register blueprints
    app.register_blueprint(analyzeRoute, url_prefix='')
    app.register_blueprint(reportRoute, url_prefix='')
    app.register_blueprint(uploadRoute, url_prefix='')

    # Initialize logging
    initialize_logging(app)

    @app.route("/")
    def home():
        web_data={
            'analyze_status':{
                'status': 'not start',
                'step': 0,
                'binary_files': {}, # {'filename': 'hash_filename'}
                'procs': {}, # {'hash_filename': False}
                'procs_name': [], # [{'filename': 'hash_filename'}]
                'reports': {}, # {'filename': 'report_path'}
            },
            'reports':{},
        }

        if os.path.isfile('web_data.json'):
            with open('web_data.json', 'r') as f:
                web_data = json.load(f)
        else:
            with open('web_data.json', 'w') as f:
                json.dump(web_data, f)

        return render_template('home.html', sidebar='home')
    
    @app.route("/clean")
    def clean():
        web_data={
            'analyze_status':{
                'status': 'not start',
                'step': 0,
                'binary_files': {}, # {'filename': 'hash_filename'}
                'procs': {}, # {'hash_filename': False}
                'procs_name': [], # [{'filename': 'hash_filename'}]
                'reports': {}, # {'filename': 'report_path'}
            },
            'reports':{},
        }
        with open('web_data.json', 'w') as f:
            json.dump(web_data, f)

        return redirect('/')

    return app
