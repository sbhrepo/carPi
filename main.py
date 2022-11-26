from motor_control import  drive
from flask import Flask
app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def hello_world():
    return 'Hello Car'

@app.route('/drive/<direction>/<speed>', methods=['GET'])
def driveCommand(direction, speed):
    return drive(direction, speed)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
    drive("stop", 0)
    drive("end", 0)
