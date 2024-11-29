using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class LoadIMG : MonoBehaviour
{
    public static byte[] ImgBytes;
    [SerializeField] private Texture2D loadTexture;
    [SerializeField] private Material material;
    private void Awake()
    {
        loadTexture = new Texture2D(1, 1);
    }
    void Update()
    {
        if (ImgBytes.Length != 0)
        {
            loadTexture.LoadImage(ImgBytes);
            // create 360 skybox material & load frame img
            material.mainTexture = loadTexture;
        }
        else
        {
            // Debug.Log("Not receiving frame");
        }
    }
}
