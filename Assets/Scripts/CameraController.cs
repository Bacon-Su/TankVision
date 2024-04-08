using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour
{
    [SerializeField] private Transform Camera;
    [SerializeField] private Transform CameraRig;

    bool RotateDirection = false; //left = false / right = true
    float StartAngle;
    float AnglePerFrame;

    private void Start()
    {
        StartAngle = Camera.eulerAngles.y;
    }
    private void Update()
    {
        AnglePerFrame = Camera.eulerAngles.y - StartAngle;//Detect angle change per frame
        AutoAdaptionRotate(AnglePerFrame);
        StartAngle = Camera.eulerAngles.y;
    }


    private void AutoAdaptionRotate(float Angle)
    {
        float RotateAngle = 3 * Angle - Angle;
        CameraRig.transform.RotateAround(Camera.position, Vector3.up, RotateAngle);
    }

}
