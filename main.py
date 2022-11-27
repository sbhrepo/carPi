from motor_control import  drive, control
from flask import Flask
app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello_world():
    return 'Hello Car'

@app.route('/drive/<direction>/<speed>', methods=['GET'])
def driveCommand(direction, speed):
    return drive(direction, speed)

@app.route('/control/<command>', methods=['GET'])
def controlCommand(command):
    return control(command)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
    drive("stop", 0)
    control("poweroff", 0)
