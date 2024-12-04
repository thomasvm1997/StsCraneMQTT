using HiveMQtt.Client;
using HiveMQtt.Client.Events;
using HiveMQtt.Client.Options;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Models.CustomEventArgs;
using Wpe.SharkCrane.Core.Services.HiveService.Interfaces;

namespace Wpe.SharkCrane.Core.Services.HiveService
{
    public class HiveMQService : IHiveMQService
    {
        private HiveMQClient _client;

        public event EventHandler<CustomMessageReceivedEventArgs> MessageReceived;

        public HiveMQService()
        {

            var options = new HiveMQClientOptions();
            options.Host = "4f123f803b6548d08e7004b574274936.s1.eu.hivemq.cloud";
            options.Port = 8883;
            options.UseTLS = true;
            options.UserName = "shark";
            options.Password = "FishFish1";
            _client = new HiveMQClient(options);

        }

        public async Task ConnectAsync()
        {
            await _client.ConnectAsync().ConfigureAwait(false);

            _client.OnMessageReceived += async (sender, args) =>
            {
                //var receivedPayload = args.PublishMessage.PayloadAsString;
                //var spreader = JsonSerializer.Deserialize<Spreader>(receivedPayload);

                //Console.WriteLine($"Message received on topic {receivedTopic}: {receivedPayload}");


                MessageReceived?.Invoke(this, new CustomMessageReceivedEventArgs(args.PublishMessage.PayloadAsString, args.PublishMessage.Topic));

            };
        }

        public async Task PublishAsync(string topic, string payload)
        {
            await _client.PublishAsync(topic, payload);
            Console.WriteLine($"Message published to topic {topic}: {payload}");
        }

        public async Task SubscribeAsync(string topic)
        {
            var r = await _client.SubscribeAsync(topic);
            Console.WriteLine($"Subscribed to topic: {topic}");

        }
    }
}
