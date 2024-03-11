using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class LoadIMG : MonoBehaviour
{
    public static byte[] ImgBytes;
    public Texture2D loadTexture;
    public Material material;
    private void Awake()
    {
        loadTexture = new Texture2D(1, 1);
        material = new Material(Shader.Find("Skybox/Panoramic"));
    }
    void Update()
    {
        
        //load img from dir path as bytes
        //string path = "D:\\project\\TankVision\\stitching\\result.png";
        //byte[] bytes = File.ReadAllBytes(path);
        
        // create texture with bytes
        loadTexture.LoadImage(ImgBytes);
        
        // create 360 skybox material & load frame img
        material.mainTexture = loadTexture; 
        RenderSettings.skybox = material;
    }
}
