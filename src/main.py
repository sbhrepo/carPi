import drive
from flask import Flask
from subprocess import call
app = Flask(__name__)

@app.route('/control/shutdown', methods=['GET'])
def shutdown():
    drive.stop()
    drive.powerOff()
    call("sudo shutdown --n", shell=True)
    return f"Raspberry Pi Shutdown"

@app.route('/control/poweron', methods=['GET'])
def poweron():
    return drive.powerOn()

@app.route('/control/poweroff', methods=['GET'])
def poweroff():
    return drive.powerOff()

@app.route('/drive/stop', methods=['GET'])
def stop():
    return drive.stop()

@app.route('/drive/front/<speed>', methods=['GET'])
def front(speed):
    return drive.front(speed, 0)

@app.route('/drive/back/<speed>', methods=['GET'])
def back(speed):
    return drive.back(speed, 0)

@app.route('/drive/right/<speed>', methods=['GET'])
def right(speed):
    return drive.right(speed, 0)

@app.route('/drive/left/<speed>', methods=['GET'])
def left(speed):
    return drive.left(speed, 0)

@app.route('/drive/frontRight/<speed>', methods=['GET'])
def frontRight(speed):
    return drive.frontRight(speed, 0)

@app.route('/drive/frontLeft/<speed>', methods=['GET'])
def frontLeft(speed):
    return drive.frontLeft(speed, 0)

@app.route('/drive/backRight/<speed>', methods=['GET'])
def backRight(speed):
    return drive.backRight(speed, 0)

@app.route('/drive/backLeft/<speed>', methods=['GET'])
def backLeft(speed):
    return drive.backLeft(speed, 0)

@app.route('/drive/turnRight/<speed>', methods=['GET'])
def turnRight(speed):
    return drive.turnRight(speed, 0)

@app.route('/drive/turnLeft/<speed>', methods=['GET'])
def turnLeft(speed):
    return drive.turnLeft(speed, 0)

if __name__ == '__main__':
    drive = drive.Drive()
    app.run(host='0.0.0.0', port=8090)
    drive.stop()
    drive.powerOff()
