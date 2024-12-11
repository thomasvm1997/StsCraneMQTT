using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Wpe.SharkCrane.Core.Models
{
    public abstract class BaseCraneObject
    {
        private double increment = 0;
        public double Increment 
        {
            get { return increment; }
            set 
            { 
                if(value <= 0) 
                {
                    increment = 0;
                }
                else if(value >= 2D)
                {
                    increment = 2D;
                }
                else
                {
                    increment = value;
                }
            }
        }
    }
}
