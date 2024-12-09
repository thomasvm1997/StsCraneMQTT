using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Models.CustomEventArgs;

namespace Wpe.SharkCrane.Core.Services.HiveService.Interfaces
{
    public interface IHiveMQService
    {
        event EventHandler<CustomMessageReceivedEventArgs> MessageReceived;

        public Task ConnectAsync();
        public Task SubscribeServiceAsync(string topic);
        public Task PublishServiceAsync(string topic, string payload);

    }
}
