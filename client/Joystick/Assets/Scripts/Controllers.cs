using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Linq;

public class Controllers : MonoBehaviour
{
    private Control control;

    public Text calibrateAccelerometer;
    public Text actualAccelerometer;

    public Text calibrateGyro;
    public Text actualGyro;

    public Slider sliderLeft;
    public Slider sliderRight;

    public Text sliderLeftText;
    public Text sliderRightText;

    public Image imageStatus;

    void Start()
    {
        control = FindObjectOfType<Control>();
        StartCoroutine(cicle());
    }

    public void calibrate()
    {
        control.calibrateAcceleration = Input.acceleration;
        control.calibrateGyro = Input.gyro.attitude;
    }

    public void updateSliderLeft()
    {
        sliderLeftText.text = (sliderLeft.value*100).ToString("##.##");
        control.sliderLeft = sliderLeft.value;
    }

    public void updateSliderRight()
    {
        sliderRightText.text = (sliderRight.value*100).ToString("##.##");
        control.sliderRight = sliderRight.value;
    }

    public void selectButton(GameObject button)
    {
        control.buttons[button.name] = true;
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
            Vector3 result = control.calibrateAcceleration - Input.acceleration;
            //Quaternion resultGyro = control.calibrateGyro - Input.gyro.attitude;

            calibrateAccelerometer.text = $"x:{control.calibrateAcceleration.x},y:{control.calibrateAcceleration.y},z:{control.calibrateAcceleration.z}";
            actualAccelerometer.text = $"x:{result.x},y:{result.y},z:{result.z}";

            if (control.connected)
            {
                send();
                imageStatus.color = Color.green;
            }
            else
            {
                imageStatus.color = Color.red;
            }

            control.buttons.Keys.ToList().ForEach(x => control.buttons[x] = false);

            yield return new WaitForSeconds(control.updateEach);
        }
    }

    async void send()
    {
        Vector3 result = control.calibrateAcceleration - Input.acceleration;
        await control.connection.emit(
            control.joystick.Direction.x, control.joystick.Direction.y,
            result.x, result.y, result.z,
            control.sliderLeft, control.sliderRight,
            control.buttons["1"],
            control.buttons["2"],
            control.buttons["3"],
            control.buttons["4"],
            control.buttons["5"],
            control.buttons["6"],
            control.buttons["7"],
            control.buttons["8"]
            );
    }
}
