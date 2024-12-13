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
        public void CreateGantryObject_WithValidParameters_ReturnsGantryObjectWithCorrectProperties()
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
        public void CreateGantryObject_WithLengthLowerThanMinimum_ReturnsGantryObjectWithCorrectedProperties()
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
        public void CreateGantryObject_WithLengthHighterThanMaximum_ReturnsGantryObjectWithCorrectedProperties()
        {
            // Arrange
            double distance = 102d;
            double expecteddistance = 100d;
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

            var gantry = new Gantry { Increment = 0.2d };
            gantryService.StorageGantry.Distance = 50d;
            var calculatedDistance = gantryService.StorageGantry.Distance + gantry.Increment;
            var expectedValue = calculatedDistance >= 100 ? 100 : calculatedDistance;
            const string topic = GantryRoutes.SubscribeRight;

            // Act
            var result = gantryService.ChangeMainProperties(gantry, topic);

            // Assert
            Assert.True(result.IsSuccess, "Expected ChangeMainProperties to succeed.");
            Assert.Equal(expectedValue, gantryService.StorageGantry.Distance);
        }

        [Fact]
        public void ChangeMainProperties_SubscribeLeft_UpdatesDistanceSuccessfully()
        {
            // Arrange
            var mockHiveMQService = new Mock<IHiveMQService>();
            var gantryService = new GantryService(mockHiveMQService.Object);

            var gantry = new Gantry { Increment = 0.2d };
            gantryService.StorageGantry.Distance = 50d;
            var calculatedDistance = gantryService.StorageGantry.Distance - gantry.Increment;
            var expectedValue = calculatedDistance <= 0 ? 0 : calculatedDistance;
            const string topic = GantryRoutes.SubscribeLeft;

            // Act
            var result = gantryService.ChangeMainProperties(gantry, topic);

            // Assert
            Assert.True(result.IsSuccess, "Expected ChangeMainProperties to succeed.");
            Assert.Equal(expectedValue, gantryService.StorageGantry.Distance);
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
            Assert.Equal(gantry.IsHandBrakeOn, gantryService.StorageGantry.IsHandBrakeOn);
        }

        [Fact]
        public void ChangeMainProperties_SubscribeRelease_UpdatesHandBrakeSuccessfully()
        {
            // Arrange
            var mockHiveMQService = new Mock<IHiveMQService>();
            var gantryService = new GantryService(mockHiveMQService.Object);

            var gantry = new Gantry { IsHandBrakeOn = false };
            const string topic = GantryRoutes.SubscribeUnlock;

            // Act
            var result = gantryService.ChangeMainProperties(gantry, topic);

            // Assert
            Assert.True(result.IsSuccess, "Expected ChangeMainProperties to succeed.");
            Assert.Equal(gantry.IsHandBrakeOn, gantryService.StorageGantry.IsHandBrakeOn);
        }

        [Fact]
        public void ChangeMainProperties_WithInvalidTopic_ReturnsError()
        {
            // Arrange
            var mockHiveMQService = new Mock<IHiveMQService>();
            var gantryService = new GantryService(mockHiveMQService.Object);

            var gantry = new Gantry { Increment = 0.2 };
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

