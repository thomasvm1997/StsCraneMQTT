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
using Wpe.SharkCrane.Core.Services.HiveService.Interfaces;
using Wpe.SharkCrane.Core.Services.SpreaderService.Interfaces;

namespace Wpe.SharkCrane.Core.Services.SpreaderService
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

            try
            {
                var spreader = JsonSerializer.Deserialize<Spreader>(e.Payload);

                ChangeMainProperties(spreader);

                var mainsString = JsonSerializer.Serialize(mainSpreader);

                await _hiveMQService.PublishServiceAsync(topic, mainsString);

            }
            catch (Exception ex) 
            {
                Console.WriteLine(ex.Message);

            }

        }

        private void ChangeMainProperties(Spreader messageSpreader)
        {
            if (mainSpreader != null)
            {
                mainSpreader.IsLocked = messageSpreader.IsLocked;
                mainSpreader.Width += messageSpreader.Increment;
            }
            else
            {
                throw new ArgumentNullException(nameof(mainSpreader));
            }
        }

    }
}
