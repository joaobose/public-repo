using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Random = UnityEngine.Random;
using Light2D;

public class AgentBasedDungeonGenerator : MonoBehaviour {

	public int amountOfRooms;
	public List<GameObject> prefabs;
	public GameObject tilePrefab;
	public GameObject obstaclePrefab;
	public GameObject noShadowObstacle;

	public GameObject obstaclesContainer;
	public GameObject DungeonContainer;

	public int minCorridorLength = 4;

	public int maxCorridorLength = 20;

	private int corridorThickness = 2;

	private List<Room2> rooms;
	private List<Corridor2> corridors;
	private Room2 actualRoom;
	private Room2 preliminarRoom;

	public GameObject player;

	private GameObject NewInstance;

	public GameObject corridorX;
	public GameObject corridorY;

	public List<Vector3> corridorsNodes;

	void Awake () {
		GenerateDungeon ();
        
	}
	
	void GenerateDungeon(){
		rooms = new List<Room2> ();
		corridors = new List<Corridor2> ();

		corridorsNodes = new List<Vector3> ();

		GameObject choice = prefabs [Random.Range (0, prefabs.Count - 1)];
		Data properties = choice.GetComponent<Data> ();


		actualRoom = new Room2 (0, 0, properties.width, properties.height, choice);
		rooms.Add (actualRoom);

		while (rooms.Count < amountOfRooms) {
			string dir = "none";

			while (true) {
				if (actualRoom.allowedConnections.Count != 0) {
					dir = actualRoom.allowedConnections[Random.Range(0,actualRoom.allowedConnections.Count - 1)];
					actualRoom.allowedConnections.Remove (dir);
				}

				if (dir != "none") {

					int corridorLenght = Random.Range (minCorridorLength, maxCorridorLength);
					preliminarRoom = GenerateRoom (actualRoom, dir, corridorLenght);

					if (rooms.Count == amountOfRooms - 1) {
						//el cuarto preliminar sera un boss room
					}

					foreach (Room2 room in rooms) {
						if (room.HitRect.CollideRect (preliminarRoom.HitRect)) {
							dir = "none";
							break;
						}
					}

					foreach (Corridor2 corridor in corridors) {
						if (corridor.hitRect.CollideRect (preliminarRoom.HitRect)) {
							dir = "none";
							break;
						}
					}

					if (dir != "none") {
						break;
					} else {
						continue;
					}
				} else {
					break;
				}
			}

			if (dir != "none") {
				Room2 instance = preliminarRoom;
				rooms.Add (instance);
				MakeCorridor (actualRoom, instance, dir);
			} else {
				actualRoom = rooms [Random.Range (0, rooms.Count - 1)];
			}
		}
			

		foreach (Room2 room in rooms) {
			GameObject x = Instantiate (room.prefab, new Vector3 (room.rect.X - 0.5f, room.rect.Y + 0.5f), Quaternion.identity);
			room.sceneInstance = x;
			x.transform.parent = DungeonContainer.transform;
			SpawnWalls (room);
		}

		foreach (Corridor2 corridor in corridors) {
			if (corridor.axis == "y") {
				GameObject c = Instantiate (corridorY, Vector3.zero, Quaternion.identity);
				c.GetComponent<corridorYcontroller> ().rect = corridor.rect;
				c.GetComponent<corridorYcontroller> ().Render ();
				c.transform.parent = DungeonContainer.transform;
			} else if (corridor.axis == "x") {
				GameObject c = Instantiate (corridorX, Vector3.zero, Quaternion.identity);
				c.GetComponent<CorridorXController> ().rect = corridor.rect;
				c.GetComponent<CorridorXController> ().Render ();
				c.transform.parent = DungeonContainer.transform;
			}
					
		}

		//colocamos al player dentro de un cuarto
		Room2 ch = rooms [Random.Range (0, rooms.Count - 1)];
		player.transform.position = ch.sceneInstance.transform.position + new Vector3 (3f, -3f, -10);
	}

	Room2 GenerateRoom(Room2 actualRoom, string dir, int corridorLenght){
		GameObject choice = prefabs [Random.Range (0, prefabs.Count)];
		Data properties = choice.GetComponent<Data> ();

		Room2 r = new Room2(0,0,0,0,null);

		if (dir == "up") {
			r = new Room2 (actualRoom.rect.Centerx - properties.width/2, actualRoom.rect.Y + corridorLenght + properties.height, properties.width, properties.height, choice);
		}
		if (dir == "down") {
			r = new Room2 (actualRoom.rect.Centerx - properties.width/2, actualRoom.rect.Bottom - corridorLenght , properties.width, properties.height, choice);
		}
		if (dir == "left") {
			r = new Room2 (actualRoom.rect.X - corridorLenght - properties.width, actualRoom.rect.Centery + properties.height/2, properties.width, properties.height, choice);
		}
		if (dir == "right") {
			r = new Room2 (actualRoom.rect.Right + corridorLenght, actualRoom.rect.Centery + properties.height/2, properties.width, properties.height, choice);
		}

		return r;
	}

	void MakeCorridor(Room2 actualRoom, Room2 otherRoom, string dir){
		Corridor2 r = new Corridor2(0,0,0,0,"y");
		Vector3 actualRoomPos = new Vector3();
		Vector3 otherRoomPos = new Vector3 ();


		if (dir == "up") {
			r = new Corridor2 ((actualRoom.rect.Centerx - corridorThickness/2 ), otherRoom.rect.Bottom, corridorThickness, (int)(otherRoom.rect.Bottom - actualRoom.rect.Y), "y");
			corridors.Add (r);

			for (int x = 0; x < corridorThickness; x++) {
				otherRoomPos = new Vector3 (x + otherRoom.rect.width / 2 + otherRoom.rect.X - corridorThickness/2, otherRoom.rect.Y - otherRoom.rect.height);

				for (int y = -1; y <= 1; y++) {
					actualRoomPos = new Vector3 (x + actualRoom.rect.width/2 + actualRoom.rect.X - corridorThickness/2, actualRoom.rect.Y - y);
					actualRoom.corridorNodes.Add (actualRoomPos);
				}
					
				otherRoom.corridorNodes.Add (otherRoomPos);
			}
		}
		if (dir == "down") {
			r = new Corridor2 ((actualRoom.rect.Centerx - corridorThickness/2 ), actualRoom.rect.Bottom, corridorThickness, (int)(actualRoom.rect.Bottom - otherRoom.rect.Y), "y");
			corridors.Add (r);

			for (int x = 0; x < corridorThickness; x++) {
				actualRoomPos = new Vector3 (x + actualRoom.rect.width / 2 + actualRoom.rect.X - corridorThickness/2, actualRoom.rect.Y - actualRoom.rect.height);

				for (int y = -1; y <= 1; y++) {
					otherRoomPos = new Vector3 (x + otherRoom.rect.width/2 + otherRoom.rect.X - corridorThickness/2, otherRoom.rect.Y - y);
					otherRoom.corridorNodes.Add (otherRoomPos);
				}

				actualRoom.corridorNodes.Add (actualRoomPos);
				otherRoom.corridorNodes.Add (otherRoomPos);
			}
		}
		if (dir == "left") {
			r = new Corridor2 (otherRoom.rect.Right, actualRoom.rect.Centery + corridorThickness/2, (int)(actualRoom.rect.X - otherRoom.rect.Right), corridorThickness, "x");
			corridors.Add (r);

			for (int y = 0; y < corridorThickness + 3; y++) {
				if (y >= corridorThickness) {
					actualRoomPos = new Vector3 (actualRoom.rect.X - 1, actualRoom.rect.Y - actualRoom.rect.height/2 + corridorThickness/2 + y - corridorThickness);
					otherRoomPos = new Vector3 (otherRoom.rect.X + otherRoom.rect.width, otherRoom.rect.Y - otherRoom.rect.height/2 + corridorThickness/2 + y - corridorThickness);
				} else {
					actualRoomPos = new Vector3 (actualRoom.rect.X - 1, actualRoom.rect.Y - actualRoom.rect.height/2 + corridorThickness/2 - y);
					otherRoomPos = new Vector3 (otherRoom.rect.X + otherRoom.rect.width, otherRoom.rect.Y - otherRoom.rect.height/2 + corridorThickness/2 - y);
				}
					

				actualRoom.corridorNodes.Add (actualRoomPos);
				otherRoom.corridorNodes.Add (otherRoomPos);
			}
		}
		if (dir == "right") {
			r = new Corridor2 (actualRoom.rect.Right, actualRoom.rect.Centery + corridorThickness/2, (int)(otherRoom.rect.X - actualRoom.rect.Right), corridorThickness, "x");
			corridors.Add (r);

			for (int y = 0; y < corridorThickness + 3; y++) {

				if (y >= corridorThickness) {
					otherRoomPos = new Vector3 (otherRoom.rect.X - 1, otherRoom.rect.Y - otherRoom.rect.height / 2 + corridorThickness / 2 + y - corridorThickness);
					actualRoomPos = new Vector3 (actualRoom.rect.X + actualRoom.rect.width, actualRoom.rect.Y - actualRoom.rect.height / 2 + corridorThickness / 2 + y - corridorThickness);
				} else {
					otherRoomPos = new Vector3 (otherRoom.rect.X - 1, otherRoom.rect.Y - otherRoom.rect.height / 2 + corridorThickness / 2 - y);
					actualRoomPos = new Vector3 (actualRoom.rect.X + actualRoom.rect.width, actualRoom.rect.Y - actualRoom.rect.height / 2 + corridorThickness / 2 - y);
				}

				actualRoom.corridorNodes.Add (actualRoomPos);
				otherRoom.corridorNodes.Add (otherRoomPos);
			}
		}
			
		bool failed = false;
		foreach (Corridor2 corridor in corridors) {
			if (corridor.rect.CollideRect (r.rect) && corridor != r) {
				failed = true;
				break;
			}
		}
		foreach (Room2 room in rooms) {
			if (room.smallRect.CollideRect (r.hitRect)) {
				failed = true;
				break;
			}
		}
		if (failed) {
			corridors.Remove (r);
			rooms.Remove (otherRoom);
		}
	}

	void SpawnWalls(Room2 room){
		for (int x = -1; x <= room.rect.width; x++) {
			for (int y = -1; y <= room.rect.height; y++) {
				if (x == -1 || x == room.rect.width || y == 1 || y == room.rect.height || y == -1) {
					Vector3 pos = new Vector3 (room.rect.X + x, room.rect.Y - y);
					if (!room.corridorNodes.Contains (pos)) {
						NewInstance = Instantiate (obstaclePrefab, pos, Quaternion.identity);
						NewInstance.transform.parent = obstaclesContainer.transform;

						if ((y == 1 && !(x == -1) && !(x == room.rect.width))) {
							Destroy (NewInstance);
							NewInstance = Instantiate (noShadowObstacle, pos, Quaternion.identity);
							NewInstance.transform.parent = obstaclesContainer.transform;
						}
					}
				}
			}
		}
	}
}

public class Room2 {
	public JRect rect;
	public JRect HitRect;
	public JRect smallRect;
	public List<string> allowedConnections;
	public GameObject prefab;
	public GameObject sceneInstance;
	public List<Vector3> corridorNodes;

	public Room2 (float x, float y, int width, int height, GameObject prefab){
		this.rect = new JRect (x, y, width, height);
		this.HitRect = new JRect (x - 1, y + 1 , width + 2, height + 2);
		this.smallRect = new JRect (x + 1, y - 1 , width - 2, height - 2);
		this.prefab = prefab;

		allowedConnections = new List<string> ();

		allowedConnections.Add ("up");
		allowedConnections.Add ("down");
		allowedConnections.Add ("left");
		allowedConnections.Add ("right");

		corridorNodes = new List<Vector3> ();
	}
}

public class Corridor2 {
	public JRect rect;
	public JRect hitRect;
	public string axis;
	public List<Vector3> nodes;

	public Corridor2(float x, float y, int width, int height, string axis){
		this.rect = new JRect (x, y, width, height);
		this.axis = axis;
		this.nodes = new List<Vector3> ();

		if (axis == "x") {
			this.hitRect = new JRect (x, y + 2, width, height + 2);
		} else {
			this.hitRect = this.rect;
		}
	}
}

