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
    byte[] mapDatas = new byte[0];
    float throttle = 100;
    float steer = 0;
    int stall = 1;
    int ping = -1;
    int loss = -1;
    int speed = 0;
    float volt = -1;

    List<float> x0;
    List<float> y0;
    List<float> x1;
    List<float> y1;
    public List<int> cls;
    List<int> trackId;
    List<float> deg;

    List<int> g = new List<int>(){0,0}; // goal
    List<int> tankPos = new List<int>(){0,0};
    int m; // manual
    int showMap = 0;

    public class Data
    {
        public byte[] image;
        public byte[] mapImage;
        public int throttle;
        public int steer;
        public int stall;

        public int ping;
        public int loss;
        public int speed;
        public float volt;

        public List<float> x0;
        public List<float> y0;
        public List<float> x1;
        public List<float> y1;
        public List<int> cls;
        public List<int> trackId;
        public List<float> deg;
        public List<int> g = new List<int>(){0,0}; // goal
        public List<int> tankPos = new List<int>(){0,0};
        public int m; // manual
        public int showMap;
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

                // string jsonData = sr.ReadLine();
                Data PythonJsonData = JsonUtility.FromJson<Data>(sr.ReadLine());
                if (PythonJsonData.image != null){
                    imgDatas = PythonJsonData.image;
                }
                if (PythonJsonData.mapImage != null){
                    mapDatas = PythonJsonData.mapImage;
                }
                ping = PythonJsonData.ping;
                loss = PythonJsonData.loss;
                throttle = PythonJsonData.throttle;
                steer = PythonJsonData.steer;
                stall = PythonJsonData.stall;
                speed = PythonJsonData.speed;
                volt = (float)(PythonJsonData.volt/100.0);

                x0 = PythonJsonData.x0;
                y0 = PythonJsonData.y0;
                x1 = PythonJsonData.x1;
                y1 = PythonJsonData.y1;
                cls = PythonJsonData.cls;
                trackId = PythonJsonData.trackId;
                deg = PythonJsonData.deg;

                g = PythonJsonData.g;
                tankPos = PythonJsonData.tankPos;
                m = PythonJsonData.m;
                showMap = PythonJsonData.showMap;
                
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
        CarState.speed = speed;
        CarState.volt = volt;
        LoadIMG.ImgBytes = imgDatas;
        Map.ImgBytes = mapDatas;
        YoloArror.x0 = x0;
        YoloArror.y0 = y0;
        YoloArror.x1 = x1;
        YoloArror.y1 = y1;
        YoloArror.cls = cls;
        YoloArror.trackId = trackId;
        YoloArror.deg = deg;
        Map.manual = m==1?true:false;
        Map.showMap = showMap==1?true:false;

        Map.tankX = tankPos[0];
        Map.tankY = tankPos[1];
        
        Map.goalX = g[0];
        Map.goalY = g[1];
        
        
    }

    private void OnDestroy()
    {
        receiveThread.Abort();
    }
}
