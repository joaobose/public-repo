using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Random = UnityEngine.Random;



public class DungeonGeneration : MonoBehaviour {

	public GameObject prefab;
	public GameObject smallRoom;
	public GameObject bigRoom;
	public int width = 80;
	public int height = 80;
	public int maxDepth = 2;
	public int minAmountOfRooms = 8;
	public int maxTry = 3;

	public List<Vector3> roomsNodes;

	private List<Cell> leafCells;
	private List<Corridor> allCorridors;

	private Cell initialNode;

	void Awake () {
		GenerateDungeon ();
	}

	void GenerateDungeon(){
		int n = 0;

		while (n < maxTry) {
			n++;

			Cell mainCell = new Cell (0f, 0f, width, height);
			Ntree mainTree = new Ntree (mainCell, 0);
			mainCell.tree = mainTree;

			leafCells = new List<Cell> ();

			RecursiveSpacePartition (mainCell);

			GenerateRooms ();


			allCorridors = new List<Corridor> ();


			foreach (Cell cell in leafCells) {
				ConnectWithNieghbours (cell);
			}

			KillNonConnectedRooms ();

			if (leafCells.Count >= minAmountOfRooms){
				break;
			} else if (n < maxTry) {
				leafCells.Clear();
				allCorridors.Clear();
			}

		}

		RoomsConstruction ();

		//construction of corridors
		foreach (Corridor corridor in allCorridors) {
			if (corridor.rect != null)
			corridor.rect.Render (prefab);
		}
	}

	void RecursiveSpacePartition(Cell cell){

		if (Random.Range(0,100) >= 60 && cell.tree.depth > maxDepth - 2){
			return;
		}

		leafCells.Remove (cell);
		var childs = divideCell (cell);

		foreach (Cell child in childs) {
			
			leafCells.Add(child);

			if (child.tree.depth < maxDepth) {
				RecursiveSpacePartition (child);
			} else {
				continue;
			}
		}
		return;
	}

	void GenerateRooms(){

		GameObject roomPrefab;

		foreach (Cell cell in leafCells) {

			if (cell.tree.depth == maxDepth) {
				roomPrefab = smallRoom;
			} else {
				roomPrefab = bigRoom;
			}

			Data properties = roomPrefab.GetComponent<Data> ();


			int _x = (int)Random.Range (cell.rect.width / 16, cell.rect.width / 4);
			int _y = (int)Random.Range(cell.rect.height/16,cell.rect.height/4);
			int _width = properties.width;
			int _height = properties.height;


			Room new_room = new Room (cell.rect.X + (float)_x, cell.rect.Y - (float)_y, _width, _height, cell , roomPrefab, properties, this);
			cell.room = new_room;

		}

	}
		

	Cell[] divideCell(Cell father){
		Cell[] childs = {
			new Cell (father.rect.X, father.rect.Y, father.rect.width / 2, father.rect.height / 2),
			new Cell (father.rect.X + father.rect.width / 2, father.rect.Y, father.rect.width / 2, father.rect.height / 2),
			new Cell (father.rect.X, father.rect.Y - father.rect.height / 2, father.rect.width / 2, father.rect.height / 2),
			new Cell (father.rect.X + father.rect.width / 2, father.rect.Y - father.rect.height / 2, father.rect.width / 2, father.rect.height / 2)
		};

		foreach (Cell child in childs) {
			Ntree tree = new Ntree (child, father.tree.depth + 1);
			child.tree = tree;
			father.tree.childs.Add (tree);
		}

		return childs;
	}

	void KillNonConnectedRooms(){

		List<Room> connected = GetConnectedRooms ();

		List<Cell> toKill = new List<Cell> ();

		foreach(Cell cell in leafCells) {

			if (!connected.Contains (cell.room)) {
				toKill.Add (cell);
			}
		}

		foreach (Cell dead in toKill){
			leafCells.Remove (dead);
			Debug.Log ("killed");

			//destruimos los corredores
			foreach(Corridor c in dead.room.corridors){
				if (allCorridors.Contains(c))
					allCorridors.Remove (c);
			}
		}
	}


	void RoomsConstruction(){
		//construction of rooms
		foreach (Cell cell in leafCells) {
			GameObject.Instantiate (cell.room.prefab, new Vector3(cell.room.rect.X - 0.5f, cell.room.rect.Y + 0.5f),Quaternion.identity);
		}
	}

	List<Room> GetConnectedRooms(){
		Queue<Room> frontier = new Queue<Room> ();

		int r = Random.Range (0, leafCells.Count - 1);

		frontier.Enqueue (leafCells [r].room);

		List<Room> connected = new List<Room> ();
		connected.Add (leafCells [r].room);

		while (frontier.Count > 0) {
			Room current = frontier.Dequeue();

			foreach(Room neighbour in current.neighbours){
				if (!connected.Contains (neighbour)) {
					frontier.Enqueue (neighbour);
					connected.Add (neighbour);
				}
			}
		}
		return connected;
	}

	void ConnectWithNieghbours(Cell cell){

		if (cell != leafCells [0]) {
			initialNode = leafCells [0];
		} else {
			initialNode = leafCells [1];
		}

		Dictionary<string, Dictionary<string,Cell>> closer = new Dictionary<string, Dictionary<string,Cell>>();

		//creating subs - dictionary 

		Dictionary<string,Cell> closerx = new Dictionary<string, Cell> ();
		closerx.Add ("izquierda", initialNode);
		closerx.Add ("derecha", initialNode);

		Dictionary<string,Cell> closery = new Dictionary<string, Cell> ();
		closery.Add ("arriba", initialNode);
		closery.Add ("abajo", initialNode);

		closer.Add ("x", closerx);
		closer.Add ("y", closery);


		//x axis
		foreach (Cell otherCell in leafCells) {

			if (otherCell.room.neighbours.Contains (cell.room) || cell.room.neighbours.Contains(otherCell.room)) {
				continue;
			}

			int thickness =  (int)Mathf.Min (cell.room.rect.height / 4, otherCell.room.rect.height / 4);

			if (cell.room.rect.Y >= otherCell.room.rect.Y) {

				int range = (int)(otherCell.room.rect.Y - otherCell.room.properties.wallSize - cell.room.rect.Bottom - 2);

				if(range < thickness){
					continue;
				}
			} else {

				int range = (int)(cell.room.rect.Y - cell.room.properties.wallSize - otherCell.room.rect.Bottom - 2);

				if (range < thickness){
					continue;
				}
			}

			if (otherCell.room.rect.X > cell.room.rect.X) {
				if (otherCell.room.rect.X < closer ["x"] ["derecha"].room.rect.X) {
					closer ["x"] ["derecha"] = otherCell;
				}
			} else if (otherCell.room.rect.X < cell.room.rect.X) {
				if (otherCell.room.rect.X > closer["x"]["izquierda"].room.rect.X){
					closer ["x"] ["izquierda"] = otherCell;
				}
			}
		}

		if (cell.rect.X < closer ["x"] ["derecha"].rect.X) {
			if (!cell.room.neighbours.Contains (closer ["x"] ["derecha"].room) && !closer ["x"] ["derecha"].room.neighbours.Contains(cell.room)) {
				Corridor newCorridor = new Corridor (cell.room, closer ["x"] ["derecha"].room, "x", this);
				allCorridors.Add (newCorridor);
			}
			
		}

		if (cell.rect.X > closer ["x"] ["izquierda"].rect.X) {
			if (!cell.room.neighbours.Contains (closer ["x"] ["izquierda"].room) && !closer ["x"] ["izquierda"].room.neighbours.Contains(cell.room)) {
				Corridor newCorridor = new Corridor (closer ["x"] ["izquierda"].room, cell.room, "x" , this);
				allCorridors.Add (newCorridor);
			}

		}

		//y axis
		foreach (Cell otherCell in leafCells) {

			if (cell.room.neighbours.Contains (otherCell.room) || cell.room.neighbours.Contains(otherCell.room)) {
				continue;
			}

			int thickness =  (int)Mathf.Min (cell.room.rect.width / 2, otherCell.room.rect.width / 2);

			if (cell.room.rect.X >= otherCell.room.rect.X) {

				int range = (int)(otherCell.room.rect.Right - cell.room.rect.X - 2);

				if(range < thickness){
					continue;
				}
			} else {

				int range = (int)(cell.room.rect.Right - otherCell.room.rect.X - 2);

				if (range < thickness){
					continue;
				}
			}

			if (otherCell.room.rect.Y > cell.room.rect.Y) {
				if (otherCell.room.rect.Y < closer ["y"] ["arriba"].room.rect.Y) {
					closer ["y"] ["arriba"] = otherCell;
				}
			} else if (otherCell.room.rect.Y < cell.room.rect.Y) {
				if (otherCell.room.rect.Y > closer["y"]["abajo"].room.rect.Y){
					closer ["y"] ["abajo"] = otherCell;
				}
			}
		}

		if (cell.rect.Y < closer ["y"] ["arriba"].rect.Y) {
			if (!cell.room.neighbours.Contains (closer ["y"] ["arriba"].room) && !closer ["y"] ["arriba"].room.neighbours.Contains(cell.room)) {
				Corridor newCorridor = new Corridor (closer ["y"] ["arriba"].room, cell.room, "y", this);
				allCorridors.Add (newCorridor);
			}
				
		}

		if (cell.rect.Y > closer ["y"] ["abajo"].rect.Y) {

			if (!cell.room.neighbours.Contains (closer ["y"] ["abajo"].room) && !closer ["y"] ["abajo"].room.neighbours.Contains(cell.room)) {
				Corridor newCorridor = new Corridor (cell.room, closer ["y"] ["abajo"].room, "y", this);
				allCorridors.Add (newCorridor);
			}

		}
	}
}

public class Cell {

	public JRect rect;
	public Room room;
	public Ntree tree;

	public Cell (float x, float y, int width, int height){
		this.rect = new JRect (x, y, width, height);
	}
}

public class Room{

	public JRect rect;
	public Cell cell;
	public GameObject prefab;
	public Data properties;
	public List<Room> neighbours;
	public List<Corridor> corridors;
	public List<Vector3> corridorsNodes;


	public Room (float x, float y, int width, int height, Cell cell, GameObject prefab , Data data, DungeonGeneration generator){
		this.rect = new JRect (x, y, width, height);
		this.cell = cell;
		this.prefab = prefab;
		this.properties = data;
		this.neighbours = new List<Room> ();
		this.corridors = new List<Corridor> ();
		this.corridorsNodes = new List<Vector3> ();

		for (int posx = 0; posx < rect.width; posx++) {
			for (int posy = 0; posy < rect.height; posy++) {
				Vector3 node = new Vector3 (rect.X + posx, rect.Y - posy);
				generator.roomsNodes.Add (node);
	
			}
		}
	}
}

public class Ntree {

	public Cell value;
	public List<Ntree> childs;
	public int depth;

	public Ntree (Cell value, int depth){
		this.value = value;
		this.depth = depth;
		this.childs = new List<Ntree> ();
	}
}

public class Corridor{

	public JRect rect;
	private int y;
	private int x;
	private int width;
	private int height;
	public Room[] roomsConnected;//element 0 is room_from, element 1 is room_to
	private bool failed = false;

	public Corridor (Room room_from, Room room_to, string axis, DungeonGeneration generator){


		roomsConnected = new Room[] { room_from, room_to };

		if (axis == "x") {

			int thickness = (int)Mathf.Min (room_from.rect.height / 4, room_to.rect.height / 4);

			if (room_from.rect.Y >= room_to.rect.Y) {

				int range = (int)(room_to.rect.Y - room_to.properties.wallSize - room_from.rect.Bottom - 2);

				if (range < thickness) {
					y = -1000;
				} else {
					int maxPos = (int)Mathf.Max (room_from.rect.Bottom + 1, room_to.rect.Y - room_to.rect.height + 1);
					y = (int)Random.Range (maxPos + thickness , room_to.rect.Y - room_to.properties.wallSize - 1);
				}

			} else {

				int range = (int)(room_from.rect.Y - room_from.properties.wallSize - room_to.rect.Bottom - 2);

				if (range < thickness) {
					y = -1000;
				} else {
					int maxPos = (int)Mathf.Max (room_to.rect.Bottom + 1, room_from.rect.Y - room_from.rect.height + 1);
					y = (int)Random.Range (maxPos + thickness , room_from.rect.Y - room_from.properties.wallSize - 1);
				}
			}

			x = (int)room_from.rect.Right;
			width = (int)(room_to.rect.Left - x);
			height = thickness;

			//checking if the corridor ovelaps a with other room
			for (int posx = 0; posx < width; posx++) {
				for (int posy = 0; posy < height; posy++){
					Vector3 node = new Vector3 (x + posx, y - posy);

					if (generator.roomsNodes.Contains (node))
						failed = true;
				}
			}

			if (y != -1000 && !failed) {
				this.rect = new JRect ((float)x, (float)y, width, height);

				room_from.neighbours.Add (room_to);
				room_to.neighbours.Add (room_from);


				room_from.corridors.Add (this);
				room_to.corridors.Add (this);

				//guardamos los nodos que formen parte del corredor
				for (int posx = 0; posx < width; posx++) {
					for (int posy = 0; posy < height; posy++){
						Vector3 node = new Vector3 (x + posx, y - posy);
						room_to.corridorsNodes.Add (node);
						room_from.corridorsNodes.Add (node);
					}
				}


			} else {
				this.rect = null;
			}
		}

		if (axis == "y") {

			int thickness = (int)Mathf.Min (room_from.rect.width / 4, room_to.rect.width / 4);

			if (room_from.rect.X >= room_to.rect.X) {

				int range = (int)(room_to.rect.Right - room_from.rect.X - 2);

				if (range < thickness) {
					x = -1000;
				} else {
					int maxPos = (int)Mathf.Min (room_to.rect.Right - 1, room_from.rect.X + room_from.rect.width - 1);
					x = (int)Random.Range (room_from.rect.X + 1, maxPos - thickness);
				}

			} else {

				int range = (int)(room_from.rect.Right - room_to.rect.X - 2);

				if (range < thickness) {
					x = -1000;
				} else {
					int maxPos = (int)Mathf.Min (room_from.rect.Right - 1 , room_to.rect.X + room_to.rect.width - 1);
					x = (int)Random.Range (room_to.rect.X + 1, maxPos - thickness);
				}
			}

			y = (int)room_from.rect.Bottom;
			width = thickness;
			height = (int)(y - room_to.rect.Top);

			//checking if the corridor ovelaps a with other room
			for (int posx = 0; posx < width; posx++) {
				for (int posy = 0; posy < height; posy++){
					Vector3 node = new Vector3 (posx + x, y - posy);

					if (generator.roomsNodes.Contains (node))
						failed = true;
				}
			}

			if (x != -1000 && !failed) {
				this.rect = new JRect ((float)x, (float)y, width, height);

				room_from.neighbours.Add (room_to);
				room_to.neighbours.Add (room_from);

				room_from.corridors.Add (this);
				room_to.corridors.Add (this);

				//guardamos los nodos que formen parte del corredor
				for (int posx = 0; posx < width; posx++) {
					for (int posy = 0; posy < height; posy++){
						Vector3 node = new Vector3 (x + posx, y - posy);
						room_to.corridorsNodes.Add (node);
						room_from.corridorsNodes.Add (node);
					}
				}

			} else {
				this.rect = null;
			}
		}
	}
}


public class JRect {
	private float x;
	private float y;
	public int width;
	public int height;

	private float top;
	private float bottom;

	private float right;
	private float left;

	private float[] center;

	private float[] topleft;
	private float[] topright;
	private float[] bottomright;
	private float[] bottomleft;

	private float centerx;
	private float centery;


	public JRect (float x, float y, int width, int height){
		this.width = width;
		this.height = height;
		this.x = x;
		this.y = y;

		this.top = y;
		this.bottom = y - height;

		this.left = x;
		this.right = x + width;

		this.center = new float[] {x + (width/2), y - (height/2)};

		this.topleft = new float[] { x, y };

		this.topright = new float[] { right, y };

		this.bottomright = new float[] { right, bottom };

		this.bottomleft = new float[] { x, bottom };

		this.centerx = center [0];

		this.centery = center [1];

	}

	public bool CollideRect( JRect rect2 ){

		return !(this.right < rect2.X || rect2.Right < this.x || this.bottom > rect2.Top || rect2.Bottom > this.top);
	}

	public float X {
		get{
			return this.x;
		}
		set{
			this.x = value;
			UpdateX ();
		}
	}

	public float Y {
		get{
			return this.y;
		}
		set{
			this.y = value;
			UpdateY ();
		}
	}

	public float Top {
		get{
			return this.top;
		}
		set{
			this.y = value;
			UpdateY ();
		}
	}

	public float Bottom {
		get{
			return this.bottom;
		}
		set{
			this.y = value + height;
			UpdateY ();
		}
	}

	public float Right {
		get{
			return this.right;
		} 
		set{
			this.x = value - width;
			UpdateX ();
		}
	}

	public float Left {
		get{
			return this.left;
		}
		set{
			this.x = value;
			UpdateX ();
		}
	}

	public float[] Center {
		get{
			return this.center;
		}
		set{
			this.x = value [0] - width / 2;
			this.y = value [1] + height / 2;
			UpdateX ();
			UpdateY ();
		}
	}

	public float[] Topleft {
		get{
			return this.topleft;
		}
		set{
			this.x = value[0];
			this.y = value[1];
			UpdateX ();
			UpdateY ();
		}
	}

	public float[] Topright {
		get{
			return this.topright;
		}
		set{
			this.x = value [0] - width;
			this.y = value [1];
			UpdateX ();
			UpdateY ();
		}
	}

	public float[] Bottomright{
		get{
			return this.bottomright;
		}
		set{
			this.x = value [0] - width;
			this.y = value [1] + height;
			UpdateX ();
			UpdateY ();
		}
	}

	public float[] Bottomleft{
		get{
			return this.bottomleft;
		}
		set{
			this.x = value [0];
			this.y = value [1] + height;
		}
	}

	public float Centerx{
		get{
			return this.centerx;
		}
		set{
			this.x = value - width / 2;
			UpdateX ();
		}
	}

	public float Centery{
		get{
			return this.centery;
		} 
		set{
			this.y = value + height / 2;
			UpdateY ();
		}
	}

	public void UpdateY(){
		this.top = y;
		this.bottom = y - height;
		this.center [1] = y - (height / 2);
		this.topleft [1] = y;
		this.topright [1] = y;
		this.bottomright [1] = bottom;
		this.bottomleft [1] = bottom;
		this.centery = center [1];
	}

	public void UpdateX(){
		this.left = x;
		this.right = x + width;
		this.center [0] = x + (width / 2);
		this.topleft [0] = x;
		this.topright [0] = right;
		this.bottomright [0] = right;
		this.bottomleft [0] = x;
		this.centerx = center [0];
	}

	public void Render(GameObject prefab){
		for (int posx = 0; posx < width; posx++) {
			for (int posy = 0; posy < height; posy++){
				GameObject.Instantiate (prefab, new Vector3 (this.x + posx, this.y - posy, 0), Quaternion.identity);
			}
		}
	}
}
