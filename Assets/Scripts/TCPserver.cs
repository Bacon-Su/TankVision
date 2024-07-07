using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Net.Sockets;
using System.Threading;
using System.Text;
using System.Net;
using UnityEngine.UI;

public class TCPserver : MonoBehaviour
{
    Thread receiveThread;
    TcpClient client;
    TcpListener listener;
    int port;

    byte[] imgDatas = new byte[0];
    float throttle = 100;
    float steer = 0;
    int stall = 1;
    int ping = -1;
    int loss = -1;

    public class Data
    {
        public byte[] image;
        public int throttle;
        public int steer;
        public int stall;

        public int ping;
        public int loss;
    }

    // Start is called before the first frame update
    void Start()
    {
        InitTcp();
    }

    private void InitTcp()
    {
        port = 5066;
        print("Tcp initialized");
        IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse("127.0.0.1"), port);
        listener = new TcpListener(anyIP);
        listener.Start();
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
    }

    public void ReceiveData()
    {
        print("receiving...");
        while (true)
        {
            try
            {
                client = listener.AcceptTcpClient();
                NetworkStream stream = client.GetStream();
                StreamReader sr = new StreamReader(stream);

                string jsonData = sr.ReadLine();

                Data PythonJsonData = JsonUtility.FromJson<Data>(jsonData);
                if (PythonJsonData.image != null){
                    imgDatas = PythonJsonData.image;
                }

                ping = PythonJsonData.ping;
                loss = PythonJsonData.loss;
                throttle = PythonJsonData.throttle;
                steer = PythonJsonData.steer;
                stall = PythonJsonData.stall;
                

            }
            catch (Exception e)
            {
                print(e);
            }
        }
    }

    
    private void Update()
    {
        CarState.ping = ping;
        CarState.loss = loss;
        CarState.throttle = throttle;
        CarState.steer = steer;
        CarState.stall = stall;
        LoadIMG.ImgBytes = imgDatas;   
    }

    private void OnDestroy()
    {
        receiveThread.Abort();
    }
}
