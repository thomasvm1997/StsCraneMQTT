using HiveMQtt.Client;
using HiveMQtt.Client.Options;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Services.Interfaces;

namespace Wpe.SharkCrane.Core.Services
{
    public class HiveMQService : IHiveMQService
    {
        private HiveMQClient _client;
        
        public HiveMQService() 
        {
            CreateClient();
        }

        private async void CreateClient()
        {
            var options = new HiveMQClientOptions();
            options.Host = "4f123f803b6548d08e7004b574274936.s1.eu.hivemq.cloud";
            options.Port = 8883;
            options.UseTLS = true;
            options.UserName = "shark";
            options.Password = "FishFish1";

            _client = new HiveMQClient(options);
            await _client.ConnectAsync().ConfigureAwait(false);
        }

        public async Task PublishAsync(string topic, string payload)
        {
            await _client.PublishAsync(topic, payload);
        }

        public async Task SubscribeAsync(string topic)
        {
           await _client.SubscribeAsync(topic);
        }
    }
}
