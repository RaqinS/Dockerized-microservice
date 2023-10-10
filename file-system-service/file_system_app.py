import os
from flask import Flask, request, send_from_directory, render_template_string
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

UPLOAD_FOLDER = '/app/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/store', methods=['POST'])
def store_file():
    try:
        logging.debug(f"Headers: {request.headers}")
        logging.debug(f"Form: {request.form}")
        logging.debug(f"Files: {request.files}")
        if 'uploaded_file' not in request.files:
            logging.debug("No 'uploaded_file' part in the request.")
            return "No uploaded_file part", 400

        file = request.files['uploaded_file']

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        
        # Check if the directory exists
        if not os.path.exists(UPLOAD_FOLDER):
            logging.debug(f"Creating directory: {UPLOAD_FOLDER}")
            os.makedirs(UPLOAD_FOLDER)

        logging.debug(f"Saving file to {file_path}")
        logging.debug(f"Original filename: {file.filename}")
        file.save(file_path)
        logging.debug(f"File saved successfully to {file_path}")

        return file_path, 200
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return f"Internal Server Error: {str(e)}", 500

@app.route('/get/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/list', methods=['GET'])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string('''
        <h2>Uploaded Files:</h2>
        <ul>
            {% for file in files %}
            <li><a href="{{ url_for('get_file', filename=file) }}">{{ file }}</a></li>
            {% endfor %}
        </ul>
    ''', files=files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
