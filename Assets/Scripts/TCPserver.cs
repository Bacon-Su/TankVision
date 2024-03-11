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

                Data _imgData = JsonUtility.FromJson<Data>(jsonData);
                imgDatas = _imgData.image;

            }
            catch (Exception e)
            {
                print(e);
            }
        }
    }

    public class Data
    {
        public byte[] image;
    }
    private void Update()
    {
        LoadIMG.ImgBytes = imgDatas;
    }

    private void OnDestroy()
    {
        receiveThread.Abort();
    }
}
