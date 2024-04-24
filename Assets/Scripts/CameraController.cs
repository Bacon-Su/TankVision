using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour
{
    [SerializeField] private Transform Camera;
    [SerializeField] private Transform CameraOffset;

    bool RotateDirection = false; //left = false / right = true
    float StartAngle;
    float NewAngle;

    private void Start()
    {
        StartAngle = Camera.localEulerAngles.y;
    }
    private void Update()
    {
        NewAngle = Camera.localEulerAngles.y - StartAngle;//Detect angle change per frame
        
        if(NewAngle > 0f)
        {
            RotateDirection = true;
        }
        if(NewAngle > 180f)
        {
            RotateDirection = false;
            NewAngle = NewAngle - 360f;
        }
        AutoAdaptionRotate(NewAngle, RotateDirection);
    }


    private void AutoAdaptionRotate(float Angle, bool RotateDirection)
    {
        //(tan((abs(x)+3)/3) - tan(1))/2
        float AngleMultiplier = (Mathf.Tan((Mathf.Abs(Mathf.Deg2Rad * Angle) + 3f) / 3f) - Mathf.Tan(1)) / 2f * Mathf.Rad2Deg;
        
        if(AngleMultiplier > 180f)
        {
            AngleMultiplier = 180f;
        }
        if (!RotateDirection)
        {
            AngleMultiplier = -AngleMultiplier;
            AngleMultiplier = AngleMultiplier - Angle;
        }
        if (RotateDirection)
        {
            Angle = -Angle;
            AngleMultiplier = AngleMultiplier + Angle;
        }

        float RotateAngle = AngleMultiplier;

        CameraOffset.transform.localEulerAngles = new Vector3(CameraOffset.transform.localEulerAngles.x, RotateAngle, CameraOffset.transform.localEulerAngles.z);
    }

}
