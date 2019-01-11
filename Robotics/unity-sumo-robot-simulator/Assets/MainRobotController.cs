using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public struct UltrasonicResponse
{
    public bool[] SensorsOutputs;
    public float[] distances;

}

public struct FloorResponse
{
    public bool[] SensorsOutputs;
}

public class MainRobotController : MonoBehaviour {

    #region controller declarations
    public Rigidbody physicDriver;
    float width;
    float height;

    Vector3[] floorSensorsOffsets;
    Vector3[] ultrasonicSensorsOffsets;
    Vector3[] ultrasonicDirs;

    public float maxTorque = 600f;//N/cm
    public float maxRpm = 90f; //RPM
    public float wheelRadius = 5f; //cm

    [HideInInspector]
    public float maxVel;

    [HideInInspector]
    public float maxAmgularVel;

    bool onSurface = true;
    public string targetTag;
    #endregion

    Strategy initialStrategy;
    Strategy actualStrategy;

    void Start()
    {
        initialStrategy = new SlashStrategy(this);
        actualStrategy = initialStrategy;

        width = this.transform.localScale.x;
        height = this.transform.localScale.y;

        maxVel = ((maxRpm/60) * 2 * Mathf.PI) * (wheelRadius / 100);
        maxAmgularVel = ((wheelRadius / 100) / (width / 2)) * ((maxRpm / 60) * 2 * Mathf.PI);

        //floor sensors offsets (its direccion its Vector3.Down)
        float a = (width / 2 - 0.05f);
        float b = (height / 2 - 0.025f);
        floorSensorsOffsets = new Vector3[] { new Vector3(a, -b, a),
                                              new Vector3(-a,-b,a),
                                              new Vector3(-a,-b,-a),
                                              new Vector3(a,-b,-a) };

        //ultrasonic sensors offsets and directions
        float phiOffset = 0.05f;
        float lambdaOffset = width / 4;

        ultrasonicSensorsOffsets = new Vector3[] { new Vector3(phiOffset,0,width/2),
                                                   new Vector3(-phiOffset,0, width/2),
                                                   new Vector3(-width/2,0,lambdaOffset),
                                                   new Vector3(width/2,0,lambdaOffset),
                                                   new Vector3(0,0,-width/2)};

        ultrasonicDirs = new Vector3[] { Vector3.forward, Vector3.forward, -Vector3.right, Vector3.right, -Vector3.forward };

        
    }

    void OnDrawGizmosSelected()
    {
        if (floorSensorsOffsets != null && ultrasonicSensorsOffsets != null)
        {
            Gizmos.color = Color.red;
            foreach (Vector3 v in floorSensorsOffsets)
            {
                Vector3 direction = transform.TransformDirection(Vector3.down) * 0.5f;
                var c = new Vector3(v.x,v.y,v.z);
                c.Scale(new Vector3(1/transform.localScale.x, 1 / transform.localScale.y, 1 / transform.localScale.z));
                Gizmos.DrawRay(transform.TransformVector(c) + transform.position, direction);
            }

            Gizmos.color = Color.blue;
            for (int i = 0; i < ultrasonicSensorsOffsets.Length; i++)
            {
                
                Vector3 direction = transform.TransformDirection(ultrasonicDirs[i]) * 1;
                var c = new Vector3(ultrasonicSensorsOffsets[i].x, ultrasonicSensorsOffsets[i].y, ultrasonicSensorsOffsets[i].z);
                c.Scale(new Vector3(1 / transform.localScale.x, 1 / transform.localScale.y, 1 / transform.localScale.z));
                Gizmos.DrawRay(transform.TransformVector(c) + transform.position, direction);
            }
        }
    }

    void FixedUpdate()
    {
        //SetVelocity(maxVel);
        actualStrategy.Update();
        actualStrategy.actualState.Update();
    }

    public UltrasonicResponse ShootUltrasonicSensors()
    {
        UltrasonicResponse response = new UltrasonicResponse
        {
            SensorsOutputs = new bool[ultrasonicSensorsOffsets.Length],
            distances = new float[ultrasonicSensorsOffsets.Length]
        };

        for(int i = 0; i < ultrasonicSensorsOffsets.Length; i++)
        {
            Vector3 direction = transform.TransformDirection(ultrasonicDirs[i]);

            var c = new Vector3(ultrasonicSensorsOffsets[i].x, ultrasonicSensorsOffsets[i].y, ultrasonicSensorsOffsets[i].z);
            c.Scale(new Vector3(1 / transform.localScale.x, 1 / transform.localScale.y, 1 / transform.localScale.z));

            Vector3 a = transform.TransformVector(c) + transform.position;
            Ray ray = new Ray(a, direction);
            RaycastHit hitData = new RaycastHit();
            
            Physics.Raycast(ray, out hitData, Mathf.Infinity, LayerMask.GetMask(targetTag));

            if (hitData.transform != null)
            {
                if (hitData.transform.gameObject.tag == targetTag)
                {
                    response.distances[i] = hitData.distance;
                    response.SensorsOutputs[i] = true;
                }
                else
                {
                    response.distances[i] = Mathf.Infinity;
                    response.SensorsOutputs[i] = false;
                }
            }
            
        }

        return response;
    }

    public FloorResponse ShootFloorSensors()
    {
        FloorResponse response = new FloorResponse
        {
            SensorsOutputs = new bool[floorSensorsOffsets.Length]
        };

        for (int i = 0; i < floorSensorsOffsets.Length; i++)
        {
            Vector3 direction = transform.TransformDirection(-transform.up);
            var c = new Vector3(floorSensorsOffsets[i].x, floorSensorsOffsets[i].y, floorSensorsOffsets[i].z);
            c.Scale(new Vector3(1 / transform.localScale.x, 1 / transform.localScale.y, 1 / transform.localScale.z));

            Vector3 a = transform.TransformVector(c) + transform.position;
            Ray ray = new Ray(a, direction);
            RaycastHit hitData = new RaycastHit();

            Physics.Raycast(ray, out hitData, Mathf.Infinity, LayerMask.GetMask("SumoArena"));

            if (hitData.transform != null)
            {
                if (hitData.transform.gameObject.tag == "SumoArena")
                {
                    response.SensorsOutputs[i] = true;
                }
                else
                {
                    response.SensorsOutputs[i] = false;
                }
            }
        }

        return response;
    }

    public bool BigOr(bool[] a)
    {
        bool s = a[0];

        for(int i = 1; i < a.Length; i++)
        {
            s = (s || a[i]);
        }
        return s;
    }

    public bool BigAnd(bool[] a)
    {
        bool s = a[0];

        for (int i = 1; i < a.Length; i++)
        {
            s = (s && a[i]);
        }
        return s;
    }

    public void SetVelocity(float module)
    {

        if (onSurface)
        {
            #region wierd velocity torque dependence
            /*if (module != 0f && physicDriver.velocity.magnitude < Mathf.Abs(module))
            {

                physicDriver.AddForce(transform.forward * maxTorque * wheelRadius * Mathf.Sign(module), ForceMode.Force);

                if (physicDriver.velocity.magnitude > Mathf.Abs(module) && CompareUnitVectors(physicDriver.velocity.normalized, transform.forward))
                {
                    Vector3 deltaVelocity = (module * transform.forward) - physicDriver.velocity;
                    physicDriver.AddForce(deltaVelocity, ForceMode.VelocityChange);
                }
            }
            else 
            {
                
                physicDriver.velocity = Vector3.zero;
                
                //Vector3 deltaVelocity = (module * transform.forward) - physicDriver.velocity;
                //physicDriver.AddForce(deltaVelocity, ForceMode.VelocityChange);
                
            }*/
            #endregion

            #region velocity and torque are independent
            physicDriver.AddForce(transform.forward * maxTorque * wheelRadius * Mathf.Sign(module) * Time.fixedDeltaTime, ForceMode.Force);

            if (physicDriver.velocity.magnitude > Mathf.Abs(module) && CompareUnitVectors(physicDriver.velocity.normalized, transform.forward))
            {
                Vector3 deltaVelocity = (module * transform.forward) - physicDriver.velocity;
                physicDriver.AddForce(deltaVelocity, ForceMode.VelocityChange);

            }
            #endregion

            #region only Velocity Control
            //Vector3 deltaVelocity = (module * transform.forward) - physicDriver.velocity;
            //physicDriver.AddForce(deltaVelocity, ForceMode.VelocityChange);
            #endregion
        }


    }

    public void SetAngularVelocity(float module)
    {
        physicDriver.angularVelocity = Vector3.up * module;
    }

    bool CompareUnitVectors(Vector3 a, Vector3 b)
    {
        return Mathf.Abs(a.x - b.x) < 0.5 && Mathf.Abs(a.y - b.y) < 0.5 && Mathf.Abs(a.y - b.y) < 0.5;
    }

    private void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.tag != targetTag)
        {
            onSurface = true;
        }
    }

    private void OnCollisionExit(Collision collision)
    {
        if (collision.gameObject.tag != targetTag)
        {
            onSurface = false;
        }
    }


}
