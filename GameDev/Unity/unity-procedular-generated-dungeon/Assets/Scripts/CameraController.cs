using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour {

	[Range(0f,1f)]
	public float smoothNess;

	public GameObject target;


	void Start () {
		
	}
	

	void FixedUpdate () {

		Vector3 desiredPos = target.transform.position;

		Vector3 NewPos = Vector3.Lerp (desiredPos,this.transform.position,smoothNess);

		this.transform.position = NewPos;


	}
}
