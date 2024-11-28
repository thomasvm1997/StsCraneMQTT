using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Wpe.SharkCrane.Core.Models
{
    public class Spreader
    {
        private decimal width;
        public decimal Width 
        {
            get {  return width; }
            set
            {
                if(value >= 12.5m)
                {
                    width = 12.5m;
                }
                width = value;
            } 
        }
        public bool IsLocked { get; set; }

    }
}
