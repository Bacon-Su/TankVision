using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour
{
    [SerializeField] private Transform Camera;
    [SerializeField] private Transform CameraRig;

    bool RotateDirection = false; //left = false / right = true
    float StartAngle;

    private void Update()
    {
        StartAngle = Camera.eulerAngles.y;
    }
    private void FixedUpdate()
    {
        float RotateAngle = Camera.eulerAngles.y - StartAngle;

        CameraRig.transform.RotateAround(Camera.position, Vector3.up, 2 * RotateAngle);

    }
}
