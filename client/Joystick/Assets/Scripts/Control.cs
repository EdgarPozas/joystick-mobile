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
    public float sliderRight;
    public Vector3 calibrateAcceleration;
    public Quaternion calibrateGyro;
    public Dictionary<string, bool> buttons = new Dictionary<string, bool>()
    {
        {"1",false },
        {"2",false },
        {"3",false },
        {"4",false },
        {"5",false },
        {"6",false },
        {"7",false },
        {"8",false },
    };

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            SceneManager.LoadScene(SceneManager.GetActiveScene().name);
        }
    }

}
