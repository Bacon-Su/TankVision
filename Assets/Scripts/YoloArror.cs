using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class YoloArror : MonoBehaviour
{
    public GameObject ArrowObject;
    public Transform parentTransform;  // 父物件的Transform
    public Transform cameraOffestTransform;
    public Transform cameraMainTransform;
    public static List<float> x0;
    public static List<float> y0;
    public static List<float> x1;
    public static List<float> y1;
    public static List<int> cls;
    public static List<int> trackId;
    public static List<float> deg;

    List<GameObject> ArrowList = new List<GameObject>();
    void Start()
    {

    }

    void Update()
    {
        for (int i = 0; i < ArrowList.Count; i++)
        {
            Destroy(ArrowList[i],0.07f);
        }
        for (int i = 0; i < cls.Count; i++)
        {
            if (cls[i] == 0)
            {   
                float cameraRotationAngles = cameraOffestTransform.eulerAngles.y % 360;
                cameraRotationAngles = cameraRotationAngles > 180 ? cameraRotationAngles - 360 : cameraRotationAngles;
                float temp = deg[i] - (cameraRotationAngles);
                temp = Mathf.Abs(temp);
                bool isRight = temp > 180 ? true : false;
                temp = temp > 180 ? 360 - temp : temp;
                print(temp);
                if ( temp > 50) 
                {
                    ArrowList.Add(Instantiate(ArrowObject,parentTransform));
                    ArrowList[ArrowList.Count-1].transform.localPosition = new Vector3(8.5f,(y0[i]+y1[i])/144,0) ;
                    
                    if (!isRight)
                    {
                        ArrowList[ArrowList.Count-1].transform.localPosition = new Vector3(-8.5f,(y0[i]+y1[i])/144,0);
                        ArrowList[ArrowList.Count-1].transform.localScale = new Vector3(ArrowList[ArrowList.Count-1].transform.localScale.x,-ArrowList[ArrowList.Count-1].transform.localScale.y,ArrowList[ArrowList.Count-1].transform.localScale.z);
                    }
                    ArrowList[ArrowList.Count-1].SetActive(true);
                    
                }
            }
        }
        
    }
}
