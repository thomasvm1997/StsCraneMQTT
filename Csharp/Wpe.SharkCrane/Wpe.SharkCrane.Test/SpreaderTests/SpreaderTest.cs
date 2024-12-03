using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Models.CustomEventArgs;
using Wpe.SharkCrane.Core.Services;

namespace Wpe.SharkCrane.Test.SpreaderTests
{
    public class SpreaderTest
    {
        [Fact]
        public void SpreaderObject_WithValidParameters_ReturnsSpreaderObjectWithCorrectProperties()
        {
            // Arrange
            double width = 5;
            bool isLocked = false;
            

            // Act
            Spreader spreader = new Spreader { IsLocked = isLocked, Width = width };

            // Assert
            Assert.NotNull(spreader);
            Assert.Equal(width, spreader.Width);
            Assert.Equal(isLocked, spreader.IsLocked);
            
        }

        [Fact]
        public void SpreaderObject_WithWidthHigherThanMax_ReturnsSpreaderObjectWithCorrectedProperties()
        {
            // Arrange
            double width = 15;
            bool isLocked = true;
            double expectedWidth = 12.5d;

            // Act
            Spreader spreader = new Spreader { IsLocked = isLocked, Width = width };

            // Assert
            Assert.NotNull(spreader);
            Assert.Equal(expectedWidth, spreader.Width);
            Assert.Equal(isLocked, spreader.IsLocked);
        }

        
    }
}
