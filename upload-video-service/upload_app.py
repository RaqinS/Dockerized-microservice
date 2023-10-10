from flask import Flask, request, render_template_string
import mysql.connector
import requests

app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template_string('''
            <form method="post" enctype="multipart/form-data">
                Video File: <input type="file" name="file"><br>
                <input type="submit" value="Upload">
            </form>
        ''')

    file = request.files['file']
    
    # Store file to File System Service...
    storage_response = requests.post('http://file-system-service:5003/store', files={'uploaded_file': file})
    if storage_response.status_code != 200:
        return "Error storing file", 500

    filepath = storage_response.text

    # Store filename and path in MySQL...
    connection = mysql.connector.connect(user='root', password='password', host='mysql-service', database='videos')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO videos (name, path) VALUES (%s, %s)', (file.filename, filepath))
    connection.commit()
    cursor.close()
    connection.close()

    return "File uploaded successfully", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
