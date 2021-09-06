using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;


public class Control : MonoBehaviour
{
    public Connection connection;
    public Settings settings;
    public Joystick joystick;

    public string url;
    public bool connected;
    public float updateEach;

    public float sliderLeft;
    public Vector3 calibrateAcceleration;
    public Dictionary<string, bool> buttons = new Dictionary<string, bool>()
    {
        {"Break",false },
        {"Parking",false },
        {"Landing Gear",false },
        {"Lights",false },
        {"Simulation Speed",false },
        {"Pause",false },
        {"Extra 2",false },
        {"Extra 3",false },
        {"Extra 4",false },
        {"Flap Up",false },
        {"Flap Down",false },
        {"Spoiler None",false },
        {"Spoiler Arm",false },
        {"Spoiler Full",false },
        {"Neutral",false },
        {"Reverse",false },
        {"Back View",false },
        {"Next View",false },
        {"Back Seat",false },
        {"Next Seat",false },
        {"Minus",false },
        {"Plus",false },
        {"Reset",false }
    };

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            SceneManager.LoadScene(SceneManager.GetActiveScene().name);
        }
    }

}
