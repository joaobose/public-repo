using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FirstPersonCamera : MonoBehaviour {


	private GameObject player;

	private Vector2 deltaMouse;
	private Vector2 mouseLook;
	private Vector2 smoothStep;

	public float smoothness = 1;

	public float sensibility = 5f;

	void Start () {
		player = this.transform.parent.gameObject;
	}

	void Update () {

		deltaMouse = new Vector2 (Input.GetAxisRaw("Mouse X") * sensibility,Input.GetAxisRaw("Mouse Y") * sensibility);

		smoothStep = Vector2.Lerp (Vector2.zero,deltaMouse,1f/smoothness);

		mouseLook += smoothStep;

		mouseLook.y = Mathf.Clamp (mouseLook.y, -90, 90);

		player.transform.localRotation = Quaternion.Euler (-mouseLook.y, mouseLook.x, 0);


	}
}
