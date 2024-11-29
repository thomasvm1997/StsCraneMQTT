using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;

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
        public void 
    }
}
