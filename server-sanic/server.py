from sanic import Sanic
from sanic.response import empty, json,file,text,empty
import vgamepad as vg
import time
import threading

app = Sanic("Joystick")

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

@app.post('/data')
async def manage_data(request):
    
    data["vx"]=float(request.form["0"][0])
    data["vy"]=float(request.form["1"][0])
    data["x"]=float(request.form["2"][0])
    data["y"]=float(request.form["3"][0])
    data["z"]=float(request.form["4"][0])
    data["sl"]=float(request.form["5"][0])
    data["sr"]=float(request.form["6"][0])
    data["btn1"]=request.form["7"][0]=="True"
    data["btn2"]=request.form["8"][0]=="True"
    data["btn3"]=request.form["9"][0]=="True"
    data["btn4"]=request.form["10"][0]=="True"
    data["btn5"]=request.form["11"][0]=="True"
    data["btn6"]=request.form["12"][0]=="True"
    data["btn7"]=request.form["13"][0]=="True"
    data["btn8"]=request.form["14"][0]=="True"

    return json({})



@app.route("/")
async def test_sockets(request):
    return await file('./test.html')

@app.get('/disconnect')
async def manage_disconnection(request):
    data["running"]=False
    return json({})

@app.get("/connect")
async def manage_connect(request):
    data["running"]=True
    controllerT=threading.Thread(target=runController)
    controllerT.start()
    return json({})

def runServer():
    app.run(host="0.0.0.0",port="5000",debug=False,access_log=False)

def runController():
    gamepad = vg.VX360Gamepad()
    while data["running"]:
        gamepad.left_joystick_float(x_value_float=-data["x"], y_value_float=data["z"])
        gamepad.right_joystick_float(x_value_float=data["vx"], y_value_float=-data["vy"])
        
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