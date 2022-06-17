from flask import Flask, request
import socket

#Initialize Flask App
app = Flask(__name__)
port = 5005

#Get Hostname
host_name = socket.gethostname()
version = "1.0"

hits = 0

@app.route('/', methods=['GET'])
def index():
    global hits
    if request.method == 'GET':
        hits+=1
        return f'{host_name} version {version} has received {hits} requests on local port {port}'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)