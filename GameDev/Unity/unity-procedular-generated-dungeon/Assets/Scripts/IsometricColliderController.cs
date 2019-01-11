using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class IsometricColliderController : MonoBehaviour {

	public int isometricLayer;
	public GameObject[] playerSprites;
	public GameObject lowestSprite;
	public int upLvl = 5;
	public int bellowLvl = 3;

	void Start () {
		
	}
	

	void OnTriggerStay2D(Collider2D other) {

		if (other.gameObject.layer == isometricLayer) {

			foreach (GameObject s in playerSprites) {

				if (other.gameObject.transform.position.y < (lowestSprite.gameObject.transform.position.y)) {
					
					s.GetComponent<SpriteRenderer> ().sortingOrder = bellowLvl;

				} else {

					s.GetComponent<SpriteRenderer> ().sortingOrder = upLvl;
				}

			}
		}
	}
}
