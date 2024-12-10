using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Wpe.SharkCrane.Core.Models
{
    public class Spreader : BaseCraneObject
    {
        private double width;
        public double Width 
        {
            get {  return width; }
            set
            {
                if(value >= 14)
                {
                    width = 14;
                }
                else if(value <= 0)
                {
                    width = 0;
                }
                else {
                width = value;
                }
            } 
        }
        
        public bool IsLocked { get; set; } = false;

    }
}
