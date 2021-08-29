using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System;
using System.Threading.Tasks;
using System.Net.Http;

public class Connection : MonoBehaviour
{
    private Control control;
    //private QSocket socket;

    private void Start()
    {
        control = FindObjectOfType<Control>();
        /*connect((result)=>
        {
            control.connected = result;
        });*/
    }

    public async Task<bool> connect()
    {
        if (control.connected)
            await disconnect();

        HttpClient client = new HttpClient();
        HttpResponseMessage response = await client.GetAsync(control.url+"/connect");

        return response.StatusCode == System.Net.HttpStatusCode.OK;
    }

    public async Task<bool> disconnect()
    {
        if (!control.connected)
            return false;
        
        HttpClient client = new HttpClient();
        HttpResponseMessage response = await client.GetAsync(control.url+ "/disconnect");

        return response.StatusCode == System.Net.HttpStatusCode.OK;
    }


    public async Task<HttpResponseMessage> emit(params object[] args )
    {
        HttpClient client = new HttpClient();
        var values = new Dictionary<string, string>();
        for (int i = 0; i < args.Length; i++)
        {
            values.Add(i.ToString(), args[i].ToString());
        }

        var body = new FormUrlEncodedContent(values);
        HttpResponseMessage response = await client.PostAsync(control.url + "/data",body);
        return response;
    }

    private async void OnDestroy()
    {
        await disconnect();
    }
}
