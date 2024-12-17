using Moq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Models.Enums;
using Wpe.SharkCrane.Core.Services.HiveService.Interfaces;
using Wpe.SharkCrane.Core.Services.TrolleyService.TrolleyRoute;
using Wpe.SharkCrane.Core.Services.TrolleyService;

namespace Wpe.SharkCrane.Test.TrolleyTests
{
    public class TrolleyTest
    {
        [Fact]
        public void CreateTrolleyObject_WithValidParameters_ReturnsTrolleyObjectWithCorrectProperties()
        {
            // Arrange
            double distance = 25d;

            // Act
            Trolley trolley = new Trolley { Distance = distance };

            // Assert
            Assert.NotNull(trolley);
            Assert.Equal(distance, trolley.Distance);
        }

        [Fact]
        public void CreateTrolleyObject_WithDistanceLowerThanMinimum_ReturnsTrolleyObjectWithCorrectedProperties()
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
        public void CreateTrolleyObject_WithDistanceHigherThanMaximum_ReturnsTrolleyObjectWithCorrectedProperties()
        {
            // Arrange
            double distance = 55d;
            double expectedDistance = 50d;

            // Act
            Trolley trolley = new Trolley { Distance = distance };

            // Assert
            Assert.NotNull(trolley);
            Assert.Equal(expectedDistance, trolley.Distance);
        }

        [Fact]
        public void CreateTrolleyObject_SetTrolleyMovement_ReturnsObjectWithCorrectMovement()
        {
            // Arrange
            TrolleyMovement movement = TrolleyMovement.Forward;

            // Act
            Trolley trolley = new Trolley { TrolleyMovement = movement };

            // Assert
            Assert.NotNull(trolley);
            Assert.Equal(movement, trolley.TrolleyMovement);
        }

        [Fact]
        public void CreateTrolleyObject_WithDefaultProperties_ReturnsNeutralMovement()
        {
            // Act
            Trolley trolley = new Trolley();

            // Assert
            Assert.NotNull(trolley);
            Assert.Equal(TrolleyMovement.Neutral, trolley.TrolleyMovement);
        }

        [Fact]
        public void ChangeMainProperties_SubscribeForward_UpdatesDistanceSuccessfully()
        {
            // Arrange
            var mockHiveMQService = new Mock<IHiveMQService>();
            var trolleyService = new TrolleyService(mockHiveMQService.Object);

            var trolley = new Trolley { Increment = 2d };
            trolleyService.StorageTrolley.Distance = 40d;
            var expectedDistance = Math.Min(50, trolleyService.StorageTrolley.Distance + trolley.Increment);
            const string topic = TrolleyRoutes.SubscribeForward;

            // Act
            var result = trolleyService.ChangeMainProperties(trolley, topic);

            // Assert
            Assert.True(result.IsSuccess, "Expected ChangeMainProperties to succeed.");
            Assert.Equal(expectedDistance, trolleyService.StorageTrolley.Distance);
        }

        [Fact]
        public void ChangeMainProperties_SubscribeBackward_UpdatesDistanceSuccessfully()
        {
            // Arrange
            var mockHiveMQService = new Mock<IHiveMQService>();
            var trolleyService = new TrolleyService(mockHiveMQService.Object);

            var trolley = new Trolley { Increment = 2d };
            trolleyService.StorageTrolley.Distance = 40d;
            var expectedDistance = Math.Max(0, trolleyService.StorageTrolley.Distance - trolley.Increment);
            const string topic = TrolleyRoutes.SubscribeBackward;

            // Act
            var result = trolleyService.ChangeMainProperties(trolley, topic);

            // Assert
            Assert.True(result.IsSuccess, "Expected ChangeMainProperties to succeed.");
            Assert.Equal(expectedDistance, trolleyService.StorageTrolley.Distance);
        }

        [Fact]
        public void ChangeMainProperties_SubscribeNeutral_ResetsIncrementAndMovement()
        {
            // Arrange
            var mockHiveMQService = new Mock<IHiveMQService>();
            var trolleyService = new TrolleyService(mockHiveMQService.Object);

            var trolley = new Trolley { TrolleyMovement = TrolleyMovement.Neutral };
            const string topic = TrolleyRoutes.SubscribeNeutral;

            // Act
            var result = trolleyService.ChangeMainProperties(trolley, topic);

            // Assert
            Assert.True(result.IsSuccess, "Expected ChangeMainProperties to succeed.");
            Assert.Equal(TrolleyMovement.Neutral, trolleyService.StorageTrolley.TrolleyMovement);
            Assert.Equal(0, trolleyService.StorageTrolley.Increment);
        }

        [Fact]
        public void ChangeMainProperties_WithInvalidTopic_ReturnsError()
        {
            // Arrange
            var mockHiveMQService = new Mock<IHiveMQService>();
            var trolleyService = new TrolleyService(mockHiveMQService.Object);

            var trolley = new Trolley { Increment = 2d };
            const string topic = "Invalid/Topic";

            // Act
            var result = trolleyService.ChangeMainProperties(trolley, topic);

            // Assert
            Assert.False(result.IsSuccess, "Expected ChangeMainProperties to fail for invalid topic.");
            Assert.Contains($"{topic} is not recognized", result.Errors);
        }

        [Fact]
        public void ChangeMainProperties_WithNullTrolley_ReturnsError()
        {
            // Arrange
            var mockHiveMQService = new Mock<IHiveMQService>();
            var trolleyService = new TrolleyService(mockHiveMQService.Object);

            const string topic = TrolleyRoutes.SubscribeForward;

            // Act
            var result = trolleyService.ChangeMainProperties(null, topic);

            // Assert
            Assert.False(result.IsSuccess, "Expected ChangeMainProperties to fail for null Trolley.");
            Assert.Contains("Could not serialize received Trolley object", result.Errors);
        }
    }
}
