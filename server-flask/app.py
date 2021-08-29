from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO
from flask_socketio import send, emit,disconnect
import vgamepad as vg
import time
import threading
import requests

app = Flask(__name__,template_folder="./")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

data={
    "x":0,
    "y":0,
    "z":0,
    "vx":0,
    "vy":0,
    "sl":0,
    "sr":0,
    "btn1":False,
    "btn2":False,
    "btn3":False,
    "btn4":False,
    "btn5":False,
    "btn6":False,
    "btn7":False,
    "btn8":False,
    "running":True
}

@socketio.on('data')
def manage_data(*args):
    data["vx"]=args[0]
    data["vy"]=args[1]
    data["x"]=args[2]
    data["y"]=args[3]
    data["z"]=args[4]
    data["sl"]=args[5]
    data["sr"]=args[6]
    data["btn1"]=args[7]
    data["btn2"]=args[8]
    data["btn3"]=args[9]
    data["btn4"]=args[10]
    data["btn5"]=args[11]
    data["btn6"]=args[12]
    data["btn7"]=args[13]
    data["btn8"]=args[14]
    
@socketio.on('connect')
def manage_connection():
    data["running"]=True
    controllerT=threading.Thread(target=runController)
    controllerT.start()

@socketio.on('disconnect')
def manage_disconnection():
    data["running"]=False
    
@app.route("/")
def test_sockets():
    return render_template('./test.html')

def runServer():
    socketio.run(app)

def runController():
    gamepad = vg.VX360Gamepad()
    while data["running"]:
        gamepad.left_joystick_float(x_value_float=-data["x"], y_value_float=data["z"])
        gamepad.right_joystick_float(x_value_float=data["vx"], y_value_float=-data["vy"])
        
        # value=data["sl"]50

        gamepad.left_trigger_float(value_float=data["sl"])
        gamepad.right_trigger_float(value_float=-data["sl"]+1)

        if data["btn1"]:
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        else:
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)

        if data["btn2"]:
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        else:
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)

        if data["btn3"]:
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        else:
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)

        if data["btn4"]:
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        else:
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)

        if data["btn5"]:
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        else:
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)

        if data["btn6"]:
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        else:
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)

        if data["btn7"]:
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        else:
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)

        if data["btn8"]:
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        else:
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)

        gamepad.update()
        time.sleep(0.01)


if __name__ == '__main__':
    runServer()