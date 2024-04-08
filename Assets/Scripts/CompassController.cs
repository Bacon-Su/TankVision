using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CompassController : MonoBehaviour
{
    [SerializeField] private Transform CamTransform;
    [SerializeField] private RawImage CompassBar;
    [SerializeField] private RectTransform CompassBarTransform;
    [SerializeField] private RectTransform testMarker;

    float AngleMultiplier;

    private void Start()
    {
        AngleMultiplier = 8.0f * 2.5f / 360f;
    }
    private void Update()
    {
        //float TargetAngle = Target.localEulerAngles.y;

        //CompassBar.uvRect = new Rect(TargetAngle / 360.0f, 0f, 1f, 1f);
        //SetMarkerPosition(testMarker, Vector3.forward * 1000);
        RotateCompass(Vector3.forward * 1000, CamTransform);
    }

    private void SetMarkerPosition(RectTransform Marker, Vector3 WorldPosition, Transform Center)
    {
        Vector3 TargetDirection = WorldPosition - Center.position;
        float Angle = Vector2.SignedAngle(new Vector2(TargetDirection.x, TargetDirection.z), new Vector2(Center.forward.x, Center.forward.z));

        float CompassMarkerPosition = Mathf.Clamp(2 * Angle / Camera.main.fieldOfView, -1, 1);
        Marker.anchoredPosition = new Vector2(CompassBarTransform.rect.width / 2 * CompassMarkerPosition, 0);
    }

    private void RotateCompass(Vector3 WorldPosition, Transform Center)
    {
        Vector3 TargetDirection = WorldPosition - Center.position;
        float Angle = Vector2.SignedAngle(new Vector2(TargetDirection.x, TargetDirection.z), new Vector2(Center.forward.x, Center.forward.z));
        //Debug.Log("Target Angle: " + Angle);

        Vector3 CompassBarPosition = CompassBar.transform.localPosition;
        CompassBarPosition.x = Angle * AngleMultiplier;
       
        CompassBar.transform.localPosition = CompassBarPosition;
    }

}
