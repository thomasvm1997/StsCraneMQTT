using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;

namespace Wpe.SharkCrane.Core.Services.Interfaces
{
    public interface IHiveMQService
    {
        public Task SubscribeAsync(string topic);
        public Task PublishAsync(string topic, string payload);
    }
}
