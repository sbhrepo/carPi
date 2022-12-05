import navigate
from flask import Flask
from flask import request
from subprocess import call

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    return nav.status()

@app.route('/control/shutdown', methods=['GET'])
def shutdown():
    nav.stop()
    nav.powerOff()
    call("sudo shutdown --n", shell=True)
    return f"Raspberry Pi Shutdown"

@app.route('/control/poweron', methods=['GET'])
def poweron():
    return nav.powerOn()

@app.route('/control/poweroff', methods=['GET'])
def poweroff():
    return nav.powerOff()

@app.route('/drive/stop', methods=['GET'])
def stop():
    return nav.stop()

@app.route('/drive/front/<speed>', methods=['GET'])
def front(speed):
    return nav.front(speed, 0)

@app.route('/drive/back/<speed>', methods=['GET'])
def back(speed):
    return nav.back(speed, 0)

@app.route('/drive/right/<speed>', methods=['GET'])
def right(speed):
    return nav.right(speed, 0)

@app.route('/drive/left/<speed>', methods=['GET'])
def left(speed):
    return nav.left(speed, 0)

@app.route('/drive/frontRight/<speed>', methods=['GET'])
def frontRight(speed):
    return nav.frontRight(speed, 0)

@app.route('/drive/frontLeft/<speed>', methods=['GET'])
def frontLeft(speed):
    return nav.frontLeft(speed, 0)

@app.route('/drive/backRight/<speed>', methods=['GET'])
def backRight(speed):
    return nav.backRight(speed, 0)

@app.route('/drive/backLeft/<speed>', methods=['GET'])
def backLeft(speed):
    return nav.backLeft(speed, 0)

@app.route('/drive/turnRight/<speed>', methods=['GET'])
def turnRight(speed):
    return nav.turnRight(speed, 0)

@app.route('/drive/turnLeft/<speed>', methods=['GET'])
def turnLeft(speed):
    return nav.turnLeft(speed, 0)

@app.route('/navigate/stop', methods=['GET'])
def NavigateStop():    
    return nav.stoptRoute()

@app.route('/navigate/start/<name>', methods=['GET'])
def navigateTo(name):
    speed = int(request.args.get("speed"))
    timeToRun = int(request.args.get("time"))
    print("name=",name," speed=",speed," time=",timeToRun)
    return nav.startRoute(name, speed, timeToRun)


if __name__ == '__main__':
    nav = navigate.Navigate()
    app.run(host='0.0.0.0', port=8090)
    nav.stop()
    nav.powerOff()
