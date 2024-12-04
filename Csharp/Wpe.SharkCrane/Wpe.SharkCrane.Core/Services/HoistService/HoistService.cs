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
using Wpe.SharkCrane.Core.Services.HoistService.HoistRoutes;
using Wpe.SharkCrane.Core.Services.HoistService.HoistRoute;

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
            
            Console.WriteLine($"HoistService received message on topic {e.Topic} : {e.Payload}");

            var hoistMessage = JsonSerializer.Deserialize<Hoist>(e.Payload);

            ChangeMainProperties(hoistMessage, e.Topic);

            var mainsString = JsonSerializer.Serialize(mainHoist);
            try
            {
                

                await _hiveMQService.PublishAsync("/hoist", mainsString);
            }

            catch (Exception ex) 
            { 
                Console.WriteLine(ex.Message);
            }

            

        }

        private void ChangeMainProperties(Hoist hoistMessage, string topic)
        {
            switch (topic)
            {

                case HoistRoutes.SubscribeUp:
                    mainHoist.Length -= hoistMessage.Increment;
                    break;

                case HoistRoutes.SubscribeDown:
                    mainHoist.Length += hoistMessage.Increment;
                    break;

                default:
                    throw new ArgumentException(topic + "not recognized");
            }
        }
    }
}
