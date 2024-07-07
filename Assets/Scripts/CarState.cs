using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class CarState : MonoBehaviour
{
    [SerializeField] private RectTransform throttleBar;
    [SerializeField] private RectTransform Stick;
    [SerializeField] private TextMeshProUGUI stallText;
    [SerializeField] private TextMeshProUGUI speedText;
    [SerializeField] private TextMeshProUGUI pingText;
    [SerializeField] private TextMeshProUGUI LossText;


    public static float throttle = 100; 
    float barVal = 0;

    public static int stall = 1;

    public static float steer = 0;
    float rotAngle = 0;

    public static int ping = -1;
    public static int loss = -1;

    // Update is called once per frame
    void Update()
    {
        if (throttle<0) barVal = -throttle;
        else barVal = throttle;
        //2.4~0.1
        barVal = (float) (-0.0023*barVal + 2.4);
        throttleBar.offsetMax = new Vector2(throttleBar.offsetMax.x, -barVal);
        throttleBar.offsetMin = new Vector2(throttleBar.offsetMin.x, (float)0.1);

        if (stall == 1)
            stallText.text = "D";
        else if (stall == 2)
            stallText.text = "R";
        else if (stall == 4)
            stallText.text = "N";
        else if (stall == 8)
            stallText.text = "P";

        rotAngle = (float) steer / 1000 * 60;
        Stick.localEulerAngles = new Vector3(0, 0, rotAngle);
        
        speedText.text = "0";

        pingText.text = ping.ToString() + " ms";
        LossText.text = loss.ToString() + " %";
    }
}
