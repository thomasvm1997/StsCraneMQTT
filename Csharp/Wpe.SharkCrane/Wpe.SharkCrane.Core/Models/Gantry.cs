using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models.Enums;

namespace Wpe.SharkCrane.Core.Models
{
    public class Gantry : BaseCraneObject
    {
        private double distance = 0;
        public double Distance 
        {
            get { return distance; }
            set
            {
                if (value <= 0)
                {
                    distance = 0;
                }
                else if(value >= 100)
                {
                    distance = 100;
                }
                else
                {
                    distance = value;
                }
            }
        }
        public bool IsHandBrakeOn {  get; set; } 

        public GantryMovement GantryMovement { get; set; } = GantryMovement.Neutral;
    }
}
