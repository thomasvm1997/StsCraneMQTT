using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;

namespace Wpe.SharkCrane.Test.GantryTests
{
    public class GantryTest
    {
        [Fact]
        public void CreateGantryObject_WithValidParameters_ReturnsSpreaderObjectWithCorrectProperties()
        {
            // Arrange
            double distance = 5d;


            // Act
            Gantry gantry = new Gantry { Distance = distance };

            // Assert
            Assert.NotNull(gantry);
            Assert.Equal(distance, gantry.Distance);
        }

        [Fact]
        public void CreateGantryObject_WithLengthLowerThanMinimum_ReturnsSpreaderObjectWithCorrectedProperties()
        {
            // Arrange
            double distance = -5d;
            double expecteddistance = 0d;
            // Act
            Gantry gantry = new Gantry { Distance = distance };

            // Assert
            Assert.NotNull(distance);
            Assert.Equal(expecteddistance, gantry.Distance);
        }


    }
}
