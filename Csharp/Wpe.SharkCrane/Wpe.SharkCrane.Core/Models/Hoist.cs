using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Wpe.SharkCrane.Core.Models
{
    public class Hoist
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
                else
                {
                    length = value;
                }
            }
        }
        public double Increment { get; set; }
    }
}
