using HiveMQtt.Client.Events;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Models.CustomEventArgs;
using Wpe.SharkCrane.Core.Services.Interfaces;

namespace Wpe.SharkCrane.Core.Services
{
    public class SpreaderService : ISpreaderService
    {
        private readonly IHiveMQService _hiveMQService;
        private Spreader mainSpreader;
        public SpreaderService(IHiveMQService hiveMQService)
        {
            _hiveMQService = hiveMQService;
            _hiveMQService.MessageReceived += OnMessageReceived;
            mainSpreader = new Spreader();
        }
            
        public async void OnMessageReceived(object sender, CustomMessageReceivedEventArgs e)
        {
            var topic = "/spreader";
            Console.WriteLine($"SpreaderService received message on topic /hub/spreader : {e.Payload}");

            
            var spreader = JsonSerializer.Deserialize<Spreader>(e.Payload);

            ChangeMainProperties(spreader);

            var mainsString = JsonSerializer.Serialize(mainSpreader);

            await _hiveMQService.PublishAsync(topic, mainsString);
            
        }

        private void ChangeMainProperties(Spreader messageSpreader)
        {
            mainSpreader.IsLocked = messageSpreader.IsLocked;
            mainSpreader.Width += messageSpreader.Width;
        }

    }
}
