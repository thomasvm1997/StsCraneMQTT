using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Models.CustomEventArgs;
using Wpe.SharkCrane.Core.Services;
using Wpe.SharkCrane.Core.Services.SpreaderService.SpreaderRoute;
using Wpe.SharkCrane.Core.Services.SpreaderService;
using Wpe.SharkCrane.Core.Services.HiveService.Interfaces;
using Wpe.SharkCrane.Core.Services.HoistService.HoistRoute;

namespace Wpe.SharkCrane.Test.SpreaderTests
{
    public class SpreaderTest
    {
        [Fact]
        public void CreateSpreaderObject_WithValidParameters_ReturnsSpreaderObjectWithCorrectProperties()
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
        public void CreateSpreaderObject_WithWidthHigherThanMax_ReturnsSpreaderObjectWithCorrectedProperties()
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

        [Fact]
        public void ChangeMainProperties_SubscribeOpen_UpdatesWidthSuccessfully()
        {
            // Arrange
            var mockHiveMQService = new Moq.Mock<IHiveMQService>();
            var spreaderService = new SpreaderService(mockHiveMQService.Object);

            
            var spreader = new Spreader { Increment = 5d };
            var expectedValue = spreaderService.MainSpreader.Width + spreader.Increment;
            const string topic = SpreaderRoutes.SubscribeOpen;

            // Act
            var result = spreaderService.ChangeMainProperties(spreader, topic);

            // Assert
            Assert.True(result.IsSuccess, "Expected ChangeMainProperties to succeed.");
            Assert.Equal(expectedValue, spreaderService.MainSpreader.Width);
        }


        [Fact]
        public void ChangeMainProperties_SubscribeClose_UpdatesWidthSuccessfully()
        {
            // Arrange
            var mockHiveMQService = new Moq.Mock<IHiveMQService>();
            var spreaderService = new SpreaderService(mockHiveMQService.Object);

            
            var spreader = new Spreader { Increment = 5 };
            var expectedValue = spreaderService.MainSpreader.Width - spreader.Increment;
            const string topic = SpreaderRoutes.SubscribeClose;

            // Act
            var result = spreaderService.ChangeMainProperties(spreader, topic);

            // Assert
            Assert.True(result.IsSuccess, "Expected ChangeMainProperties to succeed.");
            Assert.Equal(expectedValue, spreaderService.MainSpreader.Width);
        }
        [Fact]
        public void ChangeMainProperties_SubscribeLock_UpdatesLockSuccessfully()
        {
            // Arrange
            var mockHiveMQService = new Moq.Mock<IHiveMQService>();
            var spreaderService = new SpreaderService(mockHiveMQService.Object);
            
            
            var spreader = new Spreader { IsLocked = true };

            const string topic = SpreaderRoutes.SubscribeLock;

            // Act
            var result = spreaderService.ChangeMainProperties(spreader, topic);

            // Assert
            Assert.True(result.IsSuccess, "Expected ChangeMainProperties to succeed.");
            Assert.Equal(spreader.IsLocked, spreaderService.MainSpreader.IsLocked);
        }
        [Fact]
        public void ChangeMainProperties_SubscribeUnLock_UpdatesLockSuccessfully()
        {
            // Arrange
            var mockHiveMQService = new Moq.Mock<IHiveMQService>();
            var spreaderService = new SpreaderService(mockHiveMQService.Object);


            var spreader = new Spreader { IsLocked = false };

            const string topic = SpreaderRoutes.SubscribeUnlock;

            // Act
            var result = spreaderService.ChangeMainProperties(spreader, topic);

            // Assert
            Assert.True(result.IsSuccess, "Expected ChangeMainProperties to succeed.");
            Assert.Equal(spreader.IsLocked, spreaderService.MainSpreader.IsLocked);
        }
        [Fact]
        public void ChangeMainProperties_WithInvalidTopic_ReturnsError()
        {
            // Arrange
            var mockHiveMQService = new Moq.Mock<IHiveMQService>();
            var spreaderService = new SpreaderService(mockHiveMQService.Object);


            var spreader = new Spreader { IsLocked = false };

            const string topic = HoistRoutes.SubscribeDown;

            // Act
            var result = spreaderService.ChangeMainProperties(spreader, topic);

            // Assert
            Assert.False(result.IsSuccess, "Expected ChangeMainProperties to fail for invalid topic.");
            Assert.Contains($"{topic} is not recognized", result.Errors);
        }
        [Fact]
        public void ChangeMainProperties_WithNullSpreader_ReturnsError()
        {
            // Arrange
            var mockHiveMQService = new Moq.Mock<IHiveMQService>();
            var spreaderService = new SpreaderService(mockHiveMQService.Object);


            const string topic = HoistRoutes.SubscribeDown;

            // Act
            var result = spreaderService.ChangeMainProperties(null, topic);

            // Assert
            Assert.False(result.IsSuccess, "Expected ChangeMainProperties to fail for invalid topic.");
            Assert.Contains("Could not serialize received Spreader Object", result.Errors);
        }
    }
}
