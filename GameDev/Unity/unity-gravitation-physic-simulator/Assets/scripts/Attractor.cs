using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Attractor : MonoBehaviour {

	private const float G = 666.4f;

	public Rigidbody rb;

	public static List<Attractor> attractors;

	void Start(){
		rb = this.GetComponent<Rigidbody> ();
	}

	void FixedUpdate(){

		foreach (Attractor a in attractors){
			
			if (a != this)
				Attract (a);

		}
	}

	void OnEnable(){

		if (attractors == null)
			attractors = new List<Attractor> ();

		attractors.Add (this);

	}

	void OnDisable(){

		attractors.Remove (this);

	}

	void Attract(Attractor objToAttract){

		var rbToAttract = objToAttract.rb;

		Vector3 distanceAndDir = this.transform.position - objToAttract.gameObject.transform.position;

		float distance = distanceAndDir.magnitude;

		if (distance == 0)
			return;

		float forceMag = G * (rb.mass * rbToAttract.mass) / Mathf.Pow (distance, 2); 

		Vector3 gravityForce = forceMag * distanceAndDir.normalized;

		rbToAttract.AddForce (gravityForce);

	}
}
