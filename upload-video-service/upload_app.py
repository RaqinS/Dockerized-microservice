from flask import Flask, request, render_template_string, session, redirect, url_for
import mysql.connector
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secure secret key

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template_string('''
            <form method="post" enctype=multipart/form-data>
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                Video File: <input type="file" name="file"><br>
                <input type="submit" value="Upload">
            </form>
        ''')

 
    credentials = {
        'username': request.form.get('username'),
        'password': request.form.get('password')
    }


    auth_response = requests.post('http://auth-service:5002/validate', json=credentials)
    if auth_response.status_code != 200:
        return "Invalid credentials", 403

    session['authenticated'] = True

    file = request.files['file']

    if file.filename != '':
       
        file_contents = file.read()

    storage_response = requests.post('http://file-system-service:5003/store',files={'uploaded_file': (file.filename, file_contents)})
    if storage_response.status_code != 200:
        return "Error storing file", 500

    filepath = storage_response.text


    connection = mysql.connector.connect(user='root', password='password', host='mysql-service', database='videos')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO videos (name, path) VALUES (%s, %s)', (file.filename, filepath))
    connection.commit()
    cursor.close()
    connection.close()

    return "File uploaded successfully", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')