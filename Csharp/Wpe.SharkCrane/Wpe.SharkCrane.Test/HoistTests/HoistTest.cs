using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Services.HiveService.Interfaces;
using Wpe.SharkCrane.Core.Services.SpreaderService.SpreaderRoute;
using Wpe.SharkCrane.Core.Services.SpreaderService;
using Wpe.SharkCrane.Core.Services.HoistService;
using Wpe.SharkCrane.Core.Services.HoistService.HoistRoute;

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
            Hoist hoist = new Hoist { Length = length };

            // Assert
            Assert.NotNull(hoist);
            Assert.Equal(length, hoist.Length);
        }

        [Fact]
        public void CreateHoistObject_WithLengthLowerThanMinimum_ReturnsSpreaderObjectWithCorrectedProperties()
        {
            // Arrange
            double length = -5d;
            double expectedLength = 0d;
            // Act
            Hoist hoist = new Hoist { Length = length };

            // Assert
            Assert.NotNull(hoist);
            Assert.Equal(expectedLength, hoist.Length);
        }
        [Fact]
        public void ChangeMainProperties_SubscribeUp_UpdatesWidthSuccessfully()
        {
            // Arrange
            var mockHiveMQService = new Moq.Mock<IHiveMQService>();
            var hoistService = new HoistService(mockHiveMQService.Object);


            var hoist = new Hoist { Increment = 1 };

            const string topic = HoistRoutes.SubscribeUp;
            var calculatedLength = hoistService.MainHoist.Length - hoist.Increment;
            var expectedValue = calculatedLength <= 0 ? 0 : calculatedLength;

            // Act
            var result = hoistService.ChangeMainProperties(hoist, topic);

            // Assert
            Assert.True(result.IsSuccess, "Expected ChangeMainProperties to succeed.");
            Assert.Equal(expectedValue, hoistService.MainHoist.Length);
        }
        [Fact]
        public void ChangeMainProperties_SubscribeDown_UpdatesWidthSuccessfully()
        {
            // Arrange
            var mockHiveMQService = new Moq.Mock<IHiveMQService>();
            var hoistService = new HoistService(mockHiveMQService.Object);


            var hoist = new Hoist { Increment = 1 };

            const string topic = HoistRoutes.SubscribeDown;
            var expectedValue = hoistService.MainHoist.Length + hoist.Increment;

            // Act
            var result = hoistService.ChangeMainProperties(hoist, topic);

            // Assert
            Assert.True(result.IsSuccess, "Expected ChangeMainProperties to succeed.");
            Assert.Equal(expectedValue, hoistService.MainHoist.Length);
        }

        [Fact]
        public void ChangeMainProperties_WithInvalidTopic_ReturnsError()
        {
            // Arrange
            var mockHiveMQService = new Moq.Mock<IHiveMQService>();
            var hoistService = new HoistService(mockHiveMQService.Object);


            var hoist = new Hoist { Increment = 1 };

            const string topic = SpreaderRoutes.SubscribeUnlock;


            // Act
            var result = hoistService.ChangeMainProperties(hoist, topic);
            // Assert
            Assert.False(result.IsSuccess, "Expected ChangeMainProperties to fail for invalid topic.");
            Assert.Contains($"{topic} is not recognized", result.Errors);
        }

        [Fact]
        public void ChangeMainProperties_WithNullSpreader_ReturnsError()
        {
            // Arrange
            var mockHiveMQService = new Moq.Mock<IHiveMQService>();
            var hoistService = new HoistService(mockHiveMQService.Object);

            const string topic = HoistRoutes.SubscribeUp;

            // Act
            var result = hoistService.ChangeMainProperties(null, topic);

            // Assert
            Assert.False(result.IsSuccess, "Expected ChangeMainProperties to fail for invalid topic.");
            Assert.Contains("Could not serialize received Hoist object", result.Errors);
        }
    }
}
