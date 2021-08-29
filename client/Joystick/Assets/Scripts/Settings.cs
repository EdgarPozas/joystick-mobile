using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Settings : MonoBehaviour
{
    private Control control;
    public GameObject message;
    public InputField url;
    public Image img;
    public Slider slider;
    public Text frame;

    private bool testing;

    private void Start()
    {
        control = FindObjectOfType<Control>();
    }

    public void show()
    {
        url.text = control.url;
        frame.text = slider.value.ToString();
        slider.value = control.updateEach;

        if (control.connected)
        {
            img.color = Color.green;
        }
        else
        {
            img.color = Color.red;
        }

        message.SetActive(true);
    }

    public void hide()
    {
        if (testing)
            return;
        
        control.url= url.text;
        message.SetActive(false);
    }

    public async void test()
    {
        if (testing)
            return;

        testing = true;
        control.url = url.text;
        img.color = Color.white;
        control.connected = false;

        var result = await control.connection.connect();
        if (result)
        {
            img.color = Color.green;
        }
        else
        {
            img.color = Color.red;
        }

        testing = false;
        control.connected = result;
    }

    public void updateSlider()
    {
        frame.text = slider.value.ToString("##.##");
        control.updateEach = slider.value;
    }

    public void exit()
    {
        Application.Quit();
    }
}
