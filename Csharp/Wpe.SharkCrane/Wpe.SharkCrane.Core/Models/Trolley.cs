using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models.Enums;

namespace Wpe.SharkCrane.Core.Models
{
    public class Trolley : BaseCraneObject
    {
		private double distance = 0d;

		public double Distance
		{
			get { return distance; }
			set
			{ 
				if(value <= 0)
				{
					distance = 0;
				}
				else if(value >= 50)
				{
					distance = 50;
				}
				else 
				{
				distance = value;
                }
            }
		}

		public TrolleyMovement TrolleyMovement { get; set; } = TrolleyMovement.Neutral;

	}
}
