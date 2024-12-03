using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models.CustomEventArgs;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Services.HiveService.Interfaces;
using Wpe.SharkCrane.Core.Services.HoistService.Interfaces;

namespace Wpe.SharkCrane.Core.Services.HoistService
{
    public class HoistService : IHoistService
    {
        private readonly IHiveMQService _hiveMQService;
        private Hoist mainHoist;
        public HoistService(IHiveMQService hiveMQService)
        {
            _hiveMQService = hiveMQService;
            _hiveMQService.MessageReceived += OnMessageReceived;
            mainHoist = new Hoist { Length = 4d};
        }

        public async void OnMessageReceived(object sender, CustomMessageReceivedEventArgs e)
        {
            var topic = "/hoist";
            Console.WriteLine($"HoistService received message on topic /hub/hoist : {e.Payload}");


            var hoistMessage = JsonSerializer.Deserialize<Hoist>(e.Payload);

            ChangeMainProperties(hoistMessage);

            var mainsString = JsonSerializer.Serialize(mainHoist);

            await _hiveMQService.PublishAsync(topic, mainsString);

        }

        private void ChangeMainProperties(Hoist message)
        {
            if (message != null)
            {
                mainHoist.Length += message.Increment;
            }
            else
            {
                throw new ArgumentNullException(nameof(mainHoist));
            }
        }
    }
}
