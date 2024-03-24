using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CompassController : MonoBehaviour
{
    [SerializeField] private Transform MainCamera;
    [SerializeField] private Transform NorthLandmark;

    private void Update()
    {
        float CameraAngle = Vector3.SignedAngle(MainCamera.forward, NorthLandmark.position, Vector3.up);
    }

}
