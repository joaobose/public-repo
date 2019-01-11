using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CorridorXController : MonoBehaviour {

	public List<GameObject> floorTiles;
	public GameObject obstacle;
	public List<GameObject> wallsBorders;
	public List<GameObject> downWallTiles;
	public List<GameObject> upWallTiles;
	public List<GameObject> CorridorBorders;
	public List<GameObject> downFloorTiles;
	public List<GameObject> upFloorTiles;
	private GameObject instance;

	public JRect rect;

	public void Render(){

		for (int x = -1; x <= rect.width; x++) {
			for (int y = -3; y <= rect.height; y++){

				Vector3 pos = new Vector3 (rect.X + x, rect.Y - y);

				//left wall border
				if (y == -2 && x == 0) {
					instance = Instantiate (wallsBorders [0], pos, Quaternion.identity);
					instance.transform.parent = transform;
				}

				//right wall border
				if (y == -2 && x == rect.width - 1) {
					instance = Instantiate (wallsBorders [1], pos, Quaternion.identity);
					instance.transform.parent = transform;
				}

				//left corridor border
				if (x == -1 && y == 0) {
					instance = Instantiate (CorridorBorders [0], pos, Quaternion.identity);
					instance.transform.parent = transform;
				}

				//right corridor border
				if (x == rect.width  && y == 0) {
					instance = Instantiate (CorridorBorders [1], pos, Quaternion.identity);
					instance.transform.parent = transform;
				}

				//obstacles
				if ((x >= 1 && x < rect.width - 1) && (y == -3 || y == rect.height)) {
					instance = Instantiate (obstacle, pos, Quaternion.identity);
					instance.transform.parent = transform;
				}

				//up walls
				if (y == -2 && (x >= 1 && x < rect.width - 1)){
					instance = Instantiate (upWallTiles[Random.Range(0,upWallTiles.Count)], pos, Quaternion.identity);
					instance.transform.parent = transform;
				}

				//donw walls
				if (y == -1 && (x >= 1 && x < rect.width - 1)){
					instance = Instantiate (downWallTiles[Random.Range(0,downWallTiles.Count)], pos, Quaternion.identity);
					instance.transform.parent = transform;
				}

				//floor
				if ((x >= 0 && x < rect.width) && (y == 0 || y == 1)){

					if (y == 0) {
						instance = Instantiate (upFloorTiles [Random.Range (0, upFloorTiles.Count)], pos, Quaternion.identity);
						instance.transform.parent = transform;
					}

					if (y == 1) {
						instance = Instantiate (downFloorTiles [Random.Range (0, downFloorTiles.Count)], pos, Quaternion.identity);
						instance.transform.parent = transform;
					}
				}
			}
		}
	}
}
