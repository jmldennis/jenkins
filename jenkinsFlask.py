from flask import Flask, request
import socket

#Initialize Flask App
app = Flask(__name__)
port = 5005

#Get Hostname
host_name = socket.gethostname()
version = "1.1"

hits = 0

@app.route('/', methods=['GET'])
def index():
    global hits
    if request.method == 'GET':
        hits+=1
        return f'{host_name} version {version} has received {hits} requests on local port {port}'

@app.route('/hello/')
def hello_world():
    return 'Hello!\n'

@app.route('/hello/<username>') 
def hello_user(username):
    return 'Why Hello %s!\n' % username

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)