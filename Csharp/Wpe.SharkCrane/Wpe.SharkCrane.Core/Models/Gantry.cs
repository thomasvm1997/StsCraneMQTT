using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

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
                else
                {
                    distance = value;
                }
            }
        }
        public bool IsHandBrakeOn {  get; set; } 
    }
}
