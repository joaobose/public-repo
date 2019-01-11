using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class corridorYcontroller : MonoBehaviour {

	public GameObject doorPrefab;
	public GameObject obstacle;
	public GameObject noShadowObstacle;
	public List<GameObject> leftFloorTiles;
	public List<GameObject> rightFloorTiles;
	public List<GameObject> corridorBorders;
	private GameObject instance;

	public JRect rect;

	public void Render(){
		for (int x = -1; x <= rect.width; x++) {
			for (int y = -1; y <= rect.height + 2; y++) {
				
				Vector3 pos = new Vector3 (rect.X + x, rect.Y - y);

				//up corridor border
				if (y == -1 && x == 0){
					instance = Instantiate (corridorBorders[0], pos, Quaternion.identity);
					instance.transform.parent = transform;
				}

				//down corridor border
				if (y == rect.height + 2 && x == 0){
					instance = Instantiate (corridorBorders[1], pos, Quaternion.identity);
					instance.transform.parent = transform;
				}

				//noShadowObstacles
				if (y == rect.height && (x == -1 || x == rect.width)) {
					instance = Instantiate (noShadowObstacle, pos, Quaternion.identity);
					instance.transform.parent = transform;
				}

				//obstacles
				if ((y >= 1 && y < rect.height) && (x == -1 || x == rect.width)) {
					instance = Instantiate (obstacle, pos, Quaternion.identity);
					instance.transform.parent = transform;
				}

				//doors
				if ( y == rect.height){
					if (x == 0) {
						instance = Instantiate (doorPrefab, pos, Quaternion.identity);
						instance.transform.parent = transform;
					}
					if (x == 1){
						instance = Instantiate (doorPrefab, pos, Quaternion.identity);
						instance.transform.localScale = new Vector3(-1,1,1);
						instance.transform.parent = transform;
					}
				}

				//floor
				if ((y >= 0 && y < rect.height + 2)){
					if (x == 0) {
						instance = Instantiate (leftFloorTiles[Random.Range(0,leftFloorTiles.Count)], pos, Quaternion.identity);
						instance.transform.parent = transform;
					}
					if (x == 1){
						instance = Instantiate (rightFloorTiles[Random.Range(0,rightFloorTiles.Count)], pos, Quaternion.identity);
						instance.transform.parent = transform;
					}
				}
			}
		}
	}
}
