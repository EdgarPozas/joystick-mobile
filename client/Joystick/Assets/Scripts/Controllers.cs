using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Linq;

public class Controllers : MonoBehaviour
{
    private Control control;

    public Slider sliderLeft;

    public Text sliderLeftText;

    public Image imageStatus;

    public Toggle pilotWithJoystick;
    public Toggle useAccelerometer;

    void Start()
    {
        control = FindObjectOfType<Control>();
        StartCoroutine(cicle());
    }

    public void calibrate()
    {
        control.calibrateAcceleration = Input.acceleration;
    }

    public void updateSliderLeft()
    {
        float value = sliderLeft.value * 100;
        sliderLeftText.text = value==0?"0":value.ToString("###.##");
        control.sliderLeft = sliderLeft.value;
    }

    public void selectButtonPressDown(GameObject button)
    {
        control.buttons[button.name] = true;
    }

    public void selectButtonPressUp(GameObject button)
    {
        control.buttons[button.name] = false;
    }


    public async void connect()
    {
        control.connected = false;
        control.connected= await control.connection.connect();
    }

    public async void disconnect()
    {
        var result=await control.connection.disconnect();
        control.connected = !result;
    }

    IEnumerator cicle()
    {
        while (true)
        {
            if (control.connected)
            {
                send();
                imageStatus.color = Color.green;
            }
            else
            {
                imageStatus.color = Color.red;
            }

            yield return new WaitForSeconds(control.updateEach);
        }
    }

    async void send()
    {
        Vector3 result = control.calibrateAcceleration - Input.acceleration;
        Vector3 view= control.joystick.Direction;
        if (!useAccelerometer.isOn)
        {
            result = Vector3.zero;
        }
        if (pilotWithJoystick.isOn)
        {
            result = new Vector3(-control.joystick.Direction.x,0, control.joystick.Direction.y);
            view = Vector3.zero;
        }
        else
        {
            result = new Vector3(result.x, -result.y, 0);
        }

        await control.connection.emit(
            view.x, view.y,
            result.x, result.y, result.z,
            control.sliderLeft,
            control.buttons["Break"],
            control.buttons["Parking"],
            control.buttons["Landing Gear"],
            control.buttons["Lights"],
            control.buttons["Simulation Speed"],
            control.buttons["Extra 2"],
            control.buttons["Extra 3"],
            control.buttons["Extra 4"],
            control.buttons["Flap Up"],
            control.buttons["Flap Down"],
            control.buttons["Spoiler Arm"],
            control.buttons["Spoiler Full"],
            control.buttons["Reverse"],
            control.buttons["Next View"],
            control.buttons["Next Seat"],
            control.buttons["Minus"],
            control.buttons["Plus"],
            control.buttons["Reset"]
            );
    }
}
