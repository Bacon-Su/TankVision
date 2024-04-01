using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CompassController : MonoBehaviour
{
    [SerializeField] private Transform Target;
    [SerializeField] private RawImage CompassBar;
    [SerializeField] private RectTransform CompassBarTransform;
    [SerializeField] private RectTransform testMarker;

    private void Update()
    {
        float TargetAngle = Target.localEulerAngles.y;

        CompassBar.uvRect = new Rect(TargetAngle / 360.0f, 0f, 1f, 1f);
        SetMarkerPosition(testMarker, Vector3.forward * 1000);
    }

    private void SetMarkerPosition(RectTransform Marker, Vector3 WorldPosition)
    {
        Vector3 TargetDirection = WorldPosition - Target.position;
        float Angle = Vector2.SignedAngle(new Vector2(TargetDirection.x, TargetDirection.z), new Vector2(Target.forward.x, Target.forward.z));

        float CompassMarkerPosition = Mathf.Clamp(2 * Angle / Camera.main.fieldOfView, -1, 1);
        Marker.anchoredPosition = new Vector2(CompassBarTransform.rect.width / 2 * CompassMarkerPosition, 0);
    }


}
