using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour
{
    [SerializeField] private Transform mainCamera;
    [SerializeField] private Transform cameraOffset;

    float camStartAngle;
    float camNewAngle;
    float camAngle;

    float sensitive;

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
        }
        if(camAngle - camStartAngle >= 180f)
        {
            angle = 360f - camAngle; //limit the camAngle to 0 - 180 degree
        }

        if(angle >= 15f)
        {
            sensitive = 4f;
        }
        else if(angle >= 0f)
        {
            sensitive = 1f;
        }

        float result = 0;
        result = calculateAngle(camNewAngle, sensitive);

        if (mainCamera.eulerAngles.y + result < 180f)
        {
            cameraOffset.transform.localEulerAngles += new Vector3(
                cameraOffset.transform.localEulerAngles.x,
                result,
                cameraOffset.transform.localEulerAngles.z);
        }
    }


    private float calculateAngle(float camNewAngle, float sensitive)
    {
        float result = 0;
        result = camNewAngle * sensitive;

        return result;
    }

}
