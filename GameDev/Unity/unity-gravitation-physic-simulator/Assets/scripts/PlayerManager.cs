using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerManager : MonoBehaviour {

	public float velMag = 5f;
	private Rigidbody rb;


	void Start () {
		rb = this.GetComponent<Rigidbody> ();
	}
	

	void Update () {

		float x = Input.GetAxis ("x") * velMag;
		float y = Input.GetAxis ("y") * velMag;
		float z = Input.GetAxis ("z") * velMag;

		rb.velocity = (x * this.transform.right) + (y * this.transform.up) + (z * this.transform.forward);
	}

}
