using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour
{
    [SerializeField] private Transform mainCamera;
    [SerializeField] private Transform cameraOffset;

    bool rotateDirection = false; //left = false / right = true

    float camStartAngle;
    float camNewAngle;
    float camAngle;

    float offsetStartAngle;

    private void Start()
    {
        camStartAngle = mainCamera.localEulerAngles.y;
        camAngle = mainCamera.localEulerAngles.y;
    }
    private void Update()
    {
        //Detect angle change per frame
        camNewAngle = mainCamera.localEulerAngles.y - camAngle;
        camAngle = mainCamera.localEulerAngles.y;

        float angle = 0f;

        if (camAngle - camStartAngle >= 0f)
        {
            angle = camAngle;
            rotateDirection = true;
        }
        if(camAngle - camStartAngle >= 180f)
        {
            angle = 360f - camAngle; //limit the camAngle to 0 - 180 degree
            rotateDirection = false;
        }

        float result = 0;

        if(angle >= 15f)
        {
            result = calculateAngle(camNewAngle, rotateDirection, 4f);
        }
        else if(angle >= 0f)
        {
            result = calculateAngle(camNewAngle, rotateDirection, 0.01f);
        }
        Debug.Log(result);
        cameraOffset.transform.localEulerAngles += new Vector3(
            cameraOffset.transform.localEulerAngles.x,
            result,
            cameraOffset.transform.localEulerAngles.z);
        // bound the camera transform at 180 degree
        // coding...
    }


    private float calculateAngle(float camNewAngle, bool rotate_dir, float sensitive)
    {
        float result = 0;

        result = camNewAngle * sensitive;

        //if (!rotate_dir)
        //{
        //    result = -result;
        //}

        return result;
    }

}
