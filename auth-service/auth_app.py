from flask import Flask, request, jsonify

app = Flask(__name__)

# Hardcoded credentials for demonstration
USERS = {
    'user1': 'password1',
    'user2': 'password2'
}

@app.route('/validate', methods=['POST'])
def validate_credentials():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in USERS and USERS[username] == password:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'failure', 'message': 'Invalid credentials'}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
