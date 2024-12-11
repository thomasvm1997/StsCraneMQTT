using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models.Enums;

namespace Wpe.SharkCrane.Core.Models
{
    public class Spreader : BaseCraneObject
    {
        private double width = 6.06D;
        public double Width 
        {
            get {  return width; }
            set
            {
                if(value >= 14D)
                {
                    width = 14D;
                }
                else if(value <= 6.06D)
                {
                    width = 6.06D;
                }
                else {
                width = value;
                }
            } 
        }

        public SpreaderMovement SpreaderMovement { get; set; } = SpreaderMovement.Neutral;
        
        public bool IsLocked { get; set; } = false;

    }
}
