using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;

namespace Wpe.SharkCrane.Test.TrolleyTests
{
    public class TrolleyTest
    {
        [Fact]
        public void CreateTrolleyObject_WithValidParameters_ReturnsTrolleyObjectWithCorrectProperties()
        {
            // Arrange
            double distance = 5d;


            // Act
            Trolley trolley = new Trolley { Distance = distance };

            // Assert
            Assert.NotNull(trolley);
            Assert.Equal(distance, trolley.Distance);
        }

        [Fact]
        public void CreateTrolleyObject_WithLengthLowerThanMinimum_ReturnsTrolleyObjectWithCorrectedProperties()
        {
            // Arrange
            double distance = -5d;
            double expectedDistance = 0d;
            // Act
            Trolley trolley = new Trolley { Distance = distance };

            // Assert
            Assert.NotNull(trolley);
            Assert.Equal(expectedDistance, trolley.Distance);
        }
        [Fact]
        public void CreateTrolleyObject_WithLengthHigherThanMaximum_ReturnsSTrolleyObjectWithCorrectedProperties()
        {
            // Arrange
            double distance = 110d;
            double expectedDistance = 50d;
            // Act
            Trolley trolley = new Trolley { Distance = distance };

            // Assert
            Assert.NotNull(trolley);
            Assert.Equal(expectedDistance, trolley.Distance);
        }
    }
}
