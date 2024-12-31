using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Map : MonoBehaviour
{
    [SerializeField] private RectTransform tankTransform;
    [SerializeField] private RectTransform goalTransform;
    [SerializeField] private RectTransform mapTransform;
    [SerializeField] private Graphic goalGraphic;
    [SerializeField] private Image MapImage;

    public static byte[] ImgBytes;
    [SerializeField] private Texture2D loadTexture;

    public static int tankX=0, tankY=0;
    public static int goalX=0, goalY=0;
    public static bool manual = false;

    public static bool showMap = false;
    public Vector2 mapSize = new Vector2(0, 0);
    public Vector2 temp = new Vector2(0, 0);

    private void Awake()
    {
        loadTexture = new Texture2D(1, 1);
    }
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (showMap){
            mapTransform.gameObject.SetActive(true);
        }else{
            mapTransform.gameObject.SetActive(false);
        }
        mapSize.x = mapTransform.rect.width;
        mapSize.y = mapTransform.rect.height;

        temp.x = (float)(tankX/200.0 * mapSize.x);
        temp.y = (float)(tankY/200.0 * mapSize.y);
        tankTransform.anchoredPosition = temp;

        temp.x = (float)(goalX/200.0 * mapSize.x);
        temp.y = (float)(goalY/200.0 * mapSize.y);

        goalTransform.anchoredPosition = temp;

        temp.x = goalTransform.anchoredPosition.x - tankTransform.anchoredPosition.x + 0.00001f;
        temp.y = goalTransform.anchoredPosition.y - tankTransform.anchoredPosition.y+0.01f;

        // tankTransform.rotation = Quaternion.Euler(0, 0, Mathf.Atan2(temp.y, temp.x) * Mathf.Rad2Deg-90);
        if (manual)
        {
            goalGraphic.color = Color.red;
        }
        else
        {
            goalGraphic.color = Color.green;
        }
        if (ImgBytes.Length != 0)
        {
            loadTexture.LoadImage(ImgBytes);
            var sprite = Sprite.Create(loadTexture, new Rect(0, 0, loadTexture.width, loadTexture.height), new Vector2(loadTexture.width/2, loadTexture.height/2));
            MapImage.sprite = sprite;
        }
    }
}
