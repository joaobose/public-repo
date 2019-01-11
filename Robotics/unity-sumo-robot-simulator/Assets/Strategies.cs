using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;

#region abstract classes
public abstract class Strategy
{
    public abstract void Update();
    public State actualState;
}

public abstract class State
{
    public abstract void Update();
}
#endregion

public class SlashStrategy : Strategy
{
    #region states classes
    public class FowardState : State
    {
        SlashStrategy parentStrategy;
        private float tooCloseDistance = 0.15f;

        public FowardState(SlashStrategy parentStrat)
        {
            this.parentStrategy = parentStrat;
        }

        public override void Update()
        {
            parentStrategy.controller.SetVelocity(parentStrategy.controller.maxVel);

            var ultrasonicData = parentStrategy.controller.ShootUltrasonicSensors();

            var floorData = parentStrategy.controller.ShootFloorSensors();
            
            if (parentStrategy.controller.BigAnd(floorData.SensorsOutputs) == false && !((ultrasonicData.distances[1] < tooCloseDistance) && ultrasonicData.SensorsOutputs[1]) && !((ultrasonicData.distances[0] < tooCloseDistance) && ultrasonicData.SensorsOutputs[0]))
            {
                Reset();
                parentStrategy.recoverFromBorder.Reset(floorData.SensorsOutputs);
                parentStrategy.actualState = parentStrategy.recoverFromBorder;
            }

            //check  all sensors except the front ones
            for(int i = 2; i < ultrasonicData.distances.Length; i++)
            {
                if ((ultrasonicData.distances[i] < tooCloseDistance) && ultrasonicData.SensorsOutputs[i])
                {
                    parentStrategy.avoidPush.Reset(i);
                    parentStrategy.actualState = parentStrategy.avoidPush;
                }
            }

            //checking the first ones
            for (int i = 0; i < 2; i++)
            {
                if ( ultrasonicData.SensorsOutputs[i])
                {
                    parentStrategy.attack.Reset();
                    parentStrategy.actualState = parentStrategy.attack;
                }
            }
        }

        public void Reset()
        {
            parentStrategy.controller.SetVelocity(0);
            parentStrategy.controller.SetAngularVelocity(0);
        }
    }

    public class AttackState : State
    {
        SlashStrategy parentStrategy;
        private float tooCloseDistance = 0.15f;
        private int lastDir = 0;

        public AttackState(SlashStrategy parentStrat)
        {
            this.parentStrategy = parentStrat;
        }

        public override void Update()
        {
            var ultrasonicData = parentStrategy.controller.ShootUltrasonicSensors();

            var floorData = parentStrategy.controller.ShootFloorSensors();

            if (parentStrategy.controller.BigAnd(floorData.SensorsOutputs) == false && !((ultrasonicData.distances[1] < tooCloseDistance) && ultrasonicData.SensorsOutputs[1]) && !((ultrasonicData.distances[0] < tooCloseDistance) && ultrasonicData.SensorsOutputs[0]))
            {
                Reset();
                parentStrategy.recoverFromBorder.Reset(floorData.SensorsOutputs);
                parentStrategy.actualState = parentStrategy.recoverFromBorder;
            }

            //check  all sensors except the front ones
            for (int i = 2; i < ultrasonicData.distances.Length; i++)
            {
                if ((ultrasonicData.distances[i] < tooCloseDistance) && ultrasonicData.SensorsOutputs[i])
                {
                    //####change status to recover from charge (pass index to know from where the enemy is attacking)
                }
            }

            parentStrategy.controller.SetVelocity(parentStrategy.controller.maxVel);

            if (ultrasonicData.SensorsOutputs[0] && ultrasonicData.SensorsOutputs[1])
            {
                parentStrategy.controller.SetAngularVelocity(0);
                lastDir = 0;
            }
            else if (ultrasonicData.SensorsOutputs[0])
            {
                parentStrategy.controller.SetAngularVelocity(parentStrategy.controller.maxAmgularVel);
                lastDir = 1;
            }
            else if (ultrasonicData.SensorsOutputs[1])
            {
                parentStrategy.controller.SetAngularVelocity(-parentStrategy.controller.maxAmgularVel);
                lastDir = -1;
            }
            else
            {
                parentStrategy.controller.SetAngularVelocity(parentStrategy.controller.maxAmgularVel * lastDir);
            }
        }

        public void Reset()
        {
            parentStrategy.controller.SetVelocity(0);
            parentStrategy.controller.SetAngularVelocity(0);
        }
    }

    public class Turn45Degrees : State
    {
        SlashStrategy parentStrategy;
        System.Random random;
        float[] directions = new float[] { 1f, 1f };
        float toTurn;
        bool ended = false;
        bool started = false;
        float dir = 1f;

        public Turn45Degrees(SlashStrategy parentStrat)
        {
            this.parentStrategy = parentStrat;
            random = new System.Random();
            toTurn = (float)(Math.PI/4);
            dir = directions[random.Next(directions.Length)];
        }

        public override void Update()
        {
            if (!ended)
            {
                parentStrategy.controller.SetAngularVelocity(parentStrategy.controller.maxAmgularVel * dir );
                if (toTurn > 0)
                {
                    if (started)
                    {
                        toTurn -= parentStrategy.controller.maxAmgularVel * Time.fixedDeltaTime;
                    }
                }
                else
                {
                    ended = true;
                }

                started = true;
            }
            else
            {
                parentStrategy.fowardState.Reset();
                parentStrategy.actualState = parentStrategy.fowardState;
                Reset();
            }
        }

        public void Reset()
        {
            toTurn = (float)(Math.PI / 3);
            random = new System.Random();
            dir = directions[random.Next(directions.Length)];
            started = false;
            ended = false;
        }
    }

    public class RecoverFromBorder : State
    {
        SlashStrategy parentStrategy;
        System.Random random;
        float toTurn;
        bool ended = false;
        bool started = false;
        int dir = 1;
        int velDir = 1;
        float desiredVel;
        bool rotating = false;
        float backwardDistance = 0.1f;

        public RecoverFromBorder(SlashStrategy parentStrat)
        {
            this.parentStrategy = parentStrat;
            random = new System.Random();
        }

        public override void Update()
        {
            if (!ended)
            {
                if (!rotating)
                {
                    parentStrategy.controller.SetVelocity(parentStrategy.controller.maxVel * velDir);
                    parentStrategy.controller.SetAngularVelocity(0);

                    if (backwardDistance > 0)
                    {
                        if (started)
                        {
                            backwardDistance -= parentStrategy.controller.maxVel * Time.deltaTime;
                        }
                    }
                    else
                    {
                        rotating = true;
                    }
                }
                else
                {
                    var ultrasonicData = parentStrategy.controller.ShootUltrasonicSensors();
                    parentStrategy.controller.SetAngularVelocity(parentStrategy.controller.maxAmgularVel * dir);
                    parentStrategy.controller.SetVelocity(desiredVel);
                    if (toTurn > 0)
                    {
                        if (started)
                        {
                            toTurn -= parentStrategy.controller.maxAmgularVel * Time.fixedDeltaTime;
                        }
                    }
                    else
                    {
                        ended = true;
                    }

                    for (int i = 0; i < 2; i++)
                    {
                        if (ultrasonicData.SensorsOutputs[i])
                        {
                            parentStrategy.attack.Reset();
                            parentStrategy.actualState = parentStrategy.attack;
                        }
                    }
                }
                started = true;
            }
            else
            {
                parentStrategy.fowardState.Reset();
                parentStrategy.actualState = parentStrategy.fowardState;
                
            }
        }

        public void Reset(bool[] sensorData)
        {
            random = new System.Random();
            parentStrategy.controller.SetVelocity(0);
            parentStrategy.controller.SetAngularVelocity(0);

            if (!sensorData[0])
            {
                dir = -1;
                velDir = -1;
                desiredVel = 0;
                toTurn = (Mathf.PI / 2) + (float)((Mathf.PI / 4) * random.NextDouble());
            }
            else if (!sensorData[1])
            {
                dir = 1;
                velDir = -1;
                desiredVel = 0;
                toTurn = (Mathf.PI / 2) + (float)((Mathf.PI / 4) * random.NextDouble());
            }
            else if (!sensorData[2])
            {
                dir = 1;
                velDir = 1;
                desiredVel =  parentStrategy.controller.maxVel;
                toTurn = (Mathf.PI / 2) + (float)((Mathf.PI / 4) * random.NextDouble()); 
            }
            else if (!sensorData[3])
            {
                dir = -1;
                velDir = 1;
                desiredVel = parentStrategy.controller.maxVel;
                toTurn = (Mathf.PI / 2) + (float)((Mathf.PI / 4) * random.NextDouble()); 
            }
            
            ended = false;
            started = false;
            rotating = false;
            backwardDistance = 0.1f;
        }
    }

    public class AvoidPush : State
    {
        SlashStrategy parentStrategy;
        private float tooCloseDistance = 0.15f;
        private float toTurn = (float) (Math.PI / 2);
        private int enemyCommingSensorIndex;
        private bool ended = false;
        private bool started = false;

        public AvoidPush(SlashStrategy parentStrat)
        {
            this.parentStrategy = parentStrat;
        }

        public override void Update()
        {
            if (!ended)
            {
                if (enemyCommingSensorIndex == 3)//right side
                {
                    parentStrategy.controller.SetVelocity(-parentStrategy.controller.maxVel / 4);
                    parentStrategy.controller.SetAngularVelocity(3 * parentStrategy.controller.maxAmgularVel / 4);
                }

                if (enemyCommingSensorIndex == 2)//left side
                {
                    parentStrategy.controller.SetVelocity(-parentStrategy.controller.maxVel / 4);
                    parentStrategy.controller.SetAngularVelocity(-3 * parentStrategy.controller.maxAmgularVel / 4);
                }

                if (enemyCommingSensorIndex == 4)//back side
                {
                    parentStrategy.controller.SetVelocity(parentStrategy.controller.maxVel / 4);
                    parentStrategy.controller.SetAngularVelocity(-3 * parentStrategy.controller.maxAmgularVel / 4);
                }


                var ultrasonicData = parentStrategy.controller.ShootUltrasonicSensors();

                var floorData = parentStrategy.controller.ShootFloorSensors();

                if (parentStrategy.controller.BigAnd(floorData.SensorsOutputs) == false)
                {
                    parentStrategy.recoverFromBorder.Reset(floorData.SensorsOutputs);
                    parentStrategy.actualState = parentStrategy.recoverFromBorder;
                }

                //checking the front sensors
                for (int i = 0; i < 2; i++)
                {
                    if (ultrasonicData.SensorsOutputs[i])
                    {
                        parentStrategy.attack.Reset();
                        parentStrategy.actualState = parentStrategy.attack;
                    }
                }

                //check  all sensors except the front ones
                for (int i = 2; i < ultrasonicData.distances.Length; i++)
                {
                    if ((ultrasonicData.distances[i] < tooCloseDistance) && ultrasonicData.SensorsOutputs[i])
                    {
                       Reset(i);
                    }
                }

                if (toTurn > 0)
                {
                    if (started)
                    {
                        toTurn -= parentStrategy.controller.maxAmgularVel/2 * Time.fixedDeltaTime;
                    }
                }
                else
                {
                    ended = true;
                }

                started = true;
            }
            else
            {
                parentStrategy.fowardState.Reset();
                parentStrategy.actualState = parentStrategy.fowardState;
            }
        }

        public void Reset(int sensorIndex)
        {
            parentStrategy.controller.SetVelocity(0);
            parentStrategy.controller.SetAngularVelocity(0);
            enemyCommingSensorIndex = sensorIndex;

            if (enemyCommingSensorIndex == 3)//right side
            {
                parentStrategy.controller.SetVelocity(-parentStrategy.controller.maxVel / 4);
                parentStrategy.controller.SetAngularVelocity(3 * parentStrategy.controller.maxAmgularVel / 4);
            }

            if (enemyCommingSensorIndex == 2)//left side
            {
                parentStrategy.controller.SetVelocity(-parentStrategy.controller.maxVel / 4);
                parentStrategy.controller.SetAngularVelocity(-3 * parentStrategy.controller.maxAmgularVel / 4);
            }

            if (enemyCommingSensorIndex == 4)//back side
            {
                parentStrategy.controller.SetVelocity(parentStrategy.controller.maxVel / 4);
                parentStrategy.controller.SetAngularVelocity(-3 * parentStrategy.controller.maxAmgularVel / 4);
            }

            ended = false;
            started = false;
            toTurn = (float)(Math.PI / 2);

        }
    }
    #endregion

    #region states
    public FowardState fowardState;
    public Turn45Degrees turn45Degrees;
    public RecoverFromBorder recoverFromBorder;
    public AttackState attack;
    public AvoidPush avoidPush;
    #endregion

    MainRobotController controller;

    public SlashStrategy(MainRobotController controller)
    {
        this.controller = controller;
        fowardState = new FowardState(this);
        turn45Degrees = new Turn45Degrees(this);
        recoverFromBorder = new RecoverFromBorder(this);
        attack = new AttackState(this);
        avoidPush = new AvoidPush(this);
        actualState = turn45Degrees;
    }

    public override void Update()
    {
        //do nothing
    }
}


