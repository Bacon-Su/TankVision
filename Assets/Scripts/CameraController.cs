using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour
{
    [SerializeField] private Transform mainCamera;
    [SerializeField] private Transform cameraOffset;

    bool rotateDirection = false; //left = false / right = true
    float startAngle;
    float newAngle;
    float camAngle;
    float camOffsetAngle;

    private void Start()
    {
        startAngle = 0f;
    }
    private void Update()
    {
        newAngle = mainCamera.localEulerAngles.y - startAngle;//Detect angle change per frame
        camAngle = mainCamera.localEulerAngles.y;
        camOffsetAngle = cameraOffset.localEulerAngles.y;

        if (newAngle > 0f)
        {
            rotateDirection = true;
        }
        if(newAngle > 180f)
        {
            camAngle = 360f - camAngle; //limit the camAngle to 0 - 180 degree
            rotateDirection = false;
        }

        float result;
        result = calculateAngle(camAngle, rotateDirection, 15f, 3f);
        result = calculateAngle(camAngle, rotateDirection, 0f, 2f);

        cameraOffset.transform.localEulerAngles = new Vector3(
            cameraOffset.transform.localEulerAngles.x,
            result,
            cameraOffset.transform.localEulerAngles.z);
        // bound the camera transform at 180 degree
        // coding...
    }


    private float calculateAngle(float camAngle, bool rotate_dir, float start_angle, float multi)
    {
        float result = 0;

        if (camAngle >= start_angle)
        {
            result = multi * camAngle - start_angle;
        }
        if (!rotate_dir)
        {
            result = -result;
        }
        return result;
    }

}
