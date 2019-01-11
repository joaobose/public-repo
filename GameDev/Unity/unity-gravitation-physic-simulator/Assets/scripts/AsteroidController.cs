using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AsteroidController : MonoBehaviour {


	public Mesh[] meshes;

	public Material[] materials;

	public float angularSpeedVo = 1f;
	public Vector3 initialVelocity = new Vector3 (-150f, 0, 5);

	//references
	private SkinnedMeshRenderer meshRenderer;
	private MeshFilter meshFilter;
	private MeshCollider colliderA;
	private Rigidbody rb;



	void Start () {

		int indexMesh = Random.Range (0,meshes.Length);
		int indexMatt = Random.Range (0,materials.Length);

		meshRenderer = GetComponent<SkinnedMeshRenderer> ();
		meshFilter = GetComponent<MeshFilter> ();
		colliderA = GetComponent<MeshCollider> ();
		rb = GetComponent<Rigidbody> ();

		meshRenderer.sharedMesh = meshes [indexMesh];
		meshFilter.mesh = meshes [indexMesh];
		colliderA.sharedMesh = meshes [indexMesh];

		meshRenderer.material = materials [indexMatt];

		rb.angularVelocity = new Vector3 (Random.Range (-angularSpeedVo,angularSpeedVo),Random.Range (-angularSpeedVo,angularSpeedVo),
			Random.Range (-angularSpeedVo,angularSpeedVo));
		rb.velocity = initialVelocity;

	}


	void Update () {

	}
}
