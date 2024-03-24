using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CompassController : MonoBehaviour
{
    [SerializeField] private Transform Target;
    [SerializeField] private RawImage CompassBar;

    private void Update()
    {
        float CameraAngle = Target.localEulerAngles.y;

        CompassBar.uvRect = new Rect(CameraAngle / 360.0f, 0f, 1f, 1f);

    }

}
