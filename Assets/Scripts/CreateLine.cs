using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CreateLine : MonoBehaviour
{
    public LineRenderer line1;
    public GameObject P1;
    public GameObject P2;
    public GameObject P3;
    public GameObject P4;

    public int vetexCount = 12;
    public int curveRatiox = 100;
    public int curveRatioz = 100;
    List<Vector3> pointList = new List<Vector3>();

    public int P4x = 0;

    public int angle = 0;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {   
        P4x = angle + 0;
        curveRatiox = (int)(2.7*angle+100);
        curveRatioz = (int)(-2*angle+100);
        P4.transform.position = new Vector3(P4x+P2.transform.position.x, P4.transform.position.y, Mathf.Sqrt(50*50-P4x*P4x));
        
        P3.transform.position = new Vector3(
            (float)(curveRatiox/100.0)*(P2.transform.position.x+P4.transform.position.x)/2,
            (P2.transform.position.y+P4.transform.position.y)/2,
            (float)(curveRatioz/100.0)*(P2.transform.position.z+P4.transform.position.z)/2
        );
        pointList.Add(P1.transform.position);
        for (float ratio = 0; ratio<=vetexCount; ratio++)
        {
            var tan1 = Vector3.Lerp(P2.transform.position, P3.transform.position, ratio/vetexCount);
            var tan2 = Vector3.Lerp(P3.transform.position, P4.transform.position, ratio/vetexCount);
            var curve = Vector3.Lerp(tan1, tan2, ratio/vetexCount);
            pointList.Add(curve);
        }
        line1.positionCount = pointList.Count;
        line1.SetPositions(pointList.ToArray());
        pointList.Clear();
    }
}
