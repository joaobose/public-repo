using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class movement : MonoBehaviour {

	private Rigidbody2D rb;


	private Vector2 acc;
	public float accMag;
	public float fr;
	private Vector2 vel;

	private Vector2 input;

	private bool impulse;

	void Start () {
		rb = GetComponent<Rigidbody2D> ();
	}
	

	void Update () {

		input = Vector2.zero;

		if (Input.GetKey (KeyCode.W)) {
			input.y = 1;
		}
		if (Input.GetKey (KeyCode.S)) {
			input.y = -1;
		}
		if (Input.GetKey (KeyCode.A)) {
			input.x = -1;
			transform.localScale = new Vector3 (-1f, 1f, 1f);
		}
		if (Input.GetKey (KeyCode.D)) {
			input.x = 1;
			transform.localScale = new Vector3 (1f, 1f, 1f);
		}
		if (input.x != 0 && input.y != 0)
			input = new Vector2 (input.x * 0.707f, input.y * 0.707f);


		if (Input.GetKeyDown (KeyCode.Space)) {
			impulse = true;
		}
	}

	void FixedUpdate (){

		acc = ScaleVec (input, accMag);

		vel = rb.velocity;

		acc += ScaleVec (vel, fr);

		vel += ScaleVec (acc,Time.deltaTime);

		rb.velocity = vel;


		if (impulse) {
			impulse = false;
			rb.AddForce (new Vector2 (0, -50), ForceMode2D.Impulse);
		}
	}

	Vector2 ScaleVec(Vector2 vec, float scale){
		Vector2 r = new Vector2(vec.x * scale,vec.y * scale);
		return r;

	}
}
