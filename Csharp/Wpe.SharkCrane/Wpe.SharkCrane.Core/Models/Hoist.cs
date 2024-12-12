using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models.Enums;

namespace Wpe.SharkCrane.Core.Models
{
    public class Hoist : BaseCraneObject
    {
        private double length;
        public double Length 
        
        {
            get {return length;}

            set
            {
                if (value <= 0)
                {
                    length = 0;
                }
                else if(value >= 100)
                {
                    length = 100;
                }
                else
                {
                    length = value;
                }
            }
        }
        public HoistMovement HoistMovement { get; set; }
        
    }
}
