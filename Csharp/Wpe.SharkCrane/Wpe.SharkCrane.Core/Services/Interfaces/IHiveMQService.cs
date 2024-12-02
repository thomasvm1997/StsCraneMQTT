using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Models.CustomEventArgs;

namespace Wpe.SharkCrane.Core.Services.Interfaces
{
    public interface IHiveMQService
    {
        event EventHandler<CustomMessageReceivedEventArgs> MessageReceived;

        public Task ConnectAsync();
        public Task SubscribeAsync(string topic);
        public Task PublishAsync(string topic, string payload);
        
    }
}
