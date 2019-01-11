using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraFollow : MonoBehaviour {

	public Transform target;

	public float cameraSmoothVel = 0.125f;
	public Vector3 offset;

	void FixedUpdate () {


		Vector3 disiredPos = target.position + offset;
		Vector3 smoothPos = Vector3.Lerp (transform.position,disiredPos,cameraSmoothVel);

		this.transform.position = smoothPos;

		transform.LookAt (target);

	}
}
