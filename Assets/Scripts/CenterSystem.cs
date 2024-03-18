using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CenterSystem : MonoBehaviour
{
    [SerializeField] private Transform CameraTransform;
    [SerializeField] private float Distance;
    [SerializeField] private float MoveTime;

    private bool IsCentered = false;
    private Vector3 TargetPosition;
    private Vector3 Velocity = Vector3.zero;

    private void OnBecameInvisible()
    {
        IsCentered = false;
    }
    private void Update()
    {
        if (!IsCentered)
        {
            TargetPosition = FindTargetPosition();
   
            MoveToPosition(TargetPosition);

            if (ReachedTargetPosition(TargetPosition))
            {
                IsCentered = true;
            }
        }
    }
    private Vector3 FindTargetPosition()
    {
        return CameraTransform.position + (CameraTransform.forward * Distance);
    }

    private void MoveToPosition(Vector3 TargetPosition)
    {
        transform.position = Vector3.SmoothDamp(transform.position, TargetPosition, ref Velocity, MoveTime);
    }

    private bool ReachedTargetPosition(Vector3 TargetPosition)
    {
        return Vector3.Distance(TargetPosition, transform.position) < 0.1f;
    }


}

