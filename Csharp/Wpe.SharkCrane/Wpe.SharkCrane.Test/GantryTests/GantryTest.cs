using Moq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Services.GantryService.GantryRoute;
using Wpe.SharkCrane.Core.Services.GantryService;
using Wpe.SharkCrane.Core.Services.HiveService.Interfaces;

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
    
        [Fact]
        public void ChangeMainProperties_SubscribeRight_UpdatesDistanceSuccessfully()
        {
            // Arrange
            var mockHiveMQService = new Mock<IHiveMQService>();
            var gantryService = new GantryService(mockHiveMQService.Object);

            var gantry = new Gantry { Increment = 5 };
            var expectedValue = gantryService.MainGantry.Distance + gantry.Increment;
            const string topic = GantryRoutes.SubscribeRight;

            // Act
            var result = gantryService.ChangeMainProperties(gantry, topic);

            // Assert
            Assert.True(result.IsSuccess, "Expected ChangeMainProperties to succeed.");
            Assert.Equal(expectedValue, gantryService.MainGantry.Distance);
        }

        [Fact]
        public void ChangeMainProperties_SubscribeLeft_UpdatesDistanceSuccessfully()
        {
            // Arrange
            var mockHiveMQService = new Mock<IHiveMQService>();
            var gantryService = new GantryService(mockHiveMQService.Object);

            var gantry = new Gantry { Increment = 3 };
            var calculatedDistance = gantryService.MainGantry.Distance - gantry.Increment;
            var expectedValue = calculatedDistance <= 0 ? 0 : calculatedDistance;
            const string topic = GantryRoutes.SubscribeLeft;

            // Act
            var result = gantryService.ChangeMainProperties(gantry, topic);

            // Assert
            Assert.True(result.IsSuccess, "Expected ChangeMainProperties to succeed.");
            Assert.Equal(expectedValue, gantryService.MainGantry.Distance);
        }

        [Fact]
        public void ChangeMainProperties_SubscribeLock_UpdatesHandBrakeSuccessfully()
        {
            // Arrange
            var mockHiveMQService = new Mock<IHiveMQService>();
            var gantryService = new GantryService(mockHiveMQService.Object);

            var gantry = new Gantry { IsHandBrakeOn = true };
            const string topic = GantryRoutes.SubscribeLock;

            // Act
            var result = gantryService.ChangeMainProperties(gantry, topic);

            // Assert
            Assert.True(result.IsSuccess, "Expected ChangeMainProperties to succeed.");
            Assert.Equal(gantry.IsHandBrakeOn, gantryService.MainGantry.IsHandBrakeOn);
        }

        [Fact]
        public void ChangeMainProperties_SubscribeRelease_UpdatesHandBrakeSuccessfully()
        {
            // Arrange
            var mockHiveMQService = new Mock<IHiveMQService>();
            var gantryService = new GantryService(mockHiveMQService.Object);

            var gantry = new Gantry { IsHandBrakeOn = false };
            const string topic = GantryRoutes.SubscribeRelease;

            // Act
            var result = gantryService.ChangeMainProperties(gantry, topic);

            // Assert
            Assert.True(result.IsSuccess, "Expected ChangeMainProperties to succeed.");
            Assert.Equal(gantry.IsHandBrakeOn, gantryService.MainGantry.IsHandBrakeOn);
        }

        [Fact]
        public void ChangeMainProperties_WithInvalidTopic_ReturnsError()
        {
            // Arrange
            var mockHiveMQService = new Mock<IHiveMQService>();
            var gantryService = new GantryService(mockHiveMQService.Object);

            var gantry = new Gantry { Increment = 5 };
            const string topic = "Invalid/Topic";

            // Act
            var result = gantryService.ChangeMainProperties(gantry, topic);

            // Assert
            Assert.False(result.IsSuccess, "Expected ChangeMainProperties to fail for invalid topic.");
            Assert.Contains($"{topic} is not recognized", result.Errors);
        }

        [Fact]
        public void ChangeMainProperties_WithNullGantry_ReturnsError()
        {
            // Arrange
            var mockHiveMQService = new Mock<IHiveMQService>();
            var gantryService = new GantryService(mockHiveMQService.Object);

            const string topic = GantryRoutes.SubscribeRight;

            // Act
            var result = gantryService.ChangeMainProperties(null, topic);

            // Assert
            Assert.False(result.IsSuccess, "Expected ChangeMainProperties to fail for null Gantry.");
            Assert.Contains("Could not serialize received Gantry Object", result.Errors);
        }
    }

}

