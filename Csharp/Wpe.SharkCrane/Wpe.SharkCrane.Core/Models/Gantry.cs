using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Wpe.SharkCrane.Core.Models
{
    public class Gantry : BaseCraneObject
    {
        public double Distance { get; set; }
        public bool IsHandBrakeOn {  get; set; } 
    }
}
