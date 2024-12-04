using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;

namespace Wpe.SharkCrane.Test.HoistTests
{
    public class HoistTest
    {
        [Fact]
        public void CreateHoistObject_WithValidParameters_ReturnsSpreaderObjectWithCorrectProperties()
        {
            // Arrange
            double length = 5d;
            


            // Act
            Hoist hoist = new Hoist { Length = length};

            // Assert
            Assert.NotNull(hoist);
            Assert.Equal(length, hoist.Length);
            

        }

        [Fact]
        public void CreateSpreaderObject_WithValidParameters_ReturnsSpreaderObjectWithCorrectProperties()
        {
            // Arrange
            double length = 5d;

            // Act
            Hoist hoist = new Hoist { Length = length };

            // Assert
            Assert.NotNull(hoist);
            Assert.Equal(length, hoist.Length);


        }
    }
}
