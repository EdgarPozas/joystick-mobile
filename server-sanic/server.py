from pynput.keyboard import Key, Controller
from sanic import Sanic
from sanic.response import empty, json,file,text,empty
import vgamepad as vg
import time
import threading

app = Sanic("Joystick")
keyboard = Controller()

data={
    "x":0,
    "y":0,
    "z":0,
    "vx":0,
    "vy":0,
    "sl":0,
    "break":{"active":False,"key":vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP},
    "parking":{"active":False,"ctrl":True,"key":vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN},
    "landing gear":{"active":False,"key":vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT},
    "lights":{"active":False,"key":vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT},
    "simulation speed":{"active":False,"key":vg.XUSB_BUTTON.XUSB_GAMEPAD_START},
    "extra 2":{"active":False,"key":""},
    "extra 3":{"active":False,"key":""},
    "extra 4":{"active":False,"key":""},
    "flap up":{"active":False,"shift":True,"key":vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB},
    "flap down":{"active":False,"key":vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB},
    "spoiler arm":{"active":False,"shift":True,"key":vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER},
    "spoiler full":{"active":False,"key":vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER},
    # "neutral":{"active":False,"key":vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE}, #not
    "reverse":{"active":False,"key":vg.XUSB_BUTTON.XUSB_GAMEPAD_A},
    "next view":{"active":False,"key":vg.XUSB_BUTTON.XUSB_GAMEPAD_B},
    "next seat":{"active":False,"key":vg.XUSB_BUTTON.XUSB_GAMEPAD_X},
    "minus":{"active":False,"key":vg.XUSB_BUTTON.XUSB_GAMEPAD_Y},
    "plus":{"active":False,"key":vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK},
    "reset":{"active":False,"key":vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE},
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

    keys=list(data.keys())[6:len(data)-1]
    i=6
    for key in keys:
        data[key]["active"]=request.form[str(i)][0]=="True"
        i+=1

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

        keys=list(data.keys())[6:len(data)-1]
        for key in keys:
            if data[key]["key"]=="":
                continue
            if data[key]["active"]:
                gamepad.press_button(button=data[key]["key"])
            else:
                gamepad.release_button(button=data[key]["key"])
        
        gamepad.update()
        time.sleep(0.01)

if __name__ == '__main__':
    runServer()
