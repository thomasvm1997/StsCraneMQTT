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
using Wpe.SharkCrane.Core.Services.HoistService.HoistRoute;
using Wpe.SharkCrane.Core.Services.SpreaderService.SpreaderRoute;

namespace Wpe.SharkCrane.Core.Services.HoistService
{
    public class HoistService : IHoistService
    {
        public Hoist StorageHoist { get;}
        private readonly IHiveMQService _hiveMQService;
        private string publishTopic;
        public HoistService(IHiveMQService hiveMQService)
        {
            _hiveMQService = hiveMQService;
            _hiveMQService.MessageReceived += OnMessageReceived;
            StorageHoist = new Hoist { };
        }

        private async void OnMessageReceived(object sender, CustomMessageReceivedEventArgs e)
        {
            
            Console.WriteLine($"HoistService received message on topic {e.Topic} : {e.Payload}");

            Hoist hoistMessage = JsonSerializer.Deserialize<Hoist>(e.Payload);

            BaseResultModel result = ChangeMainProperties(hoistMessage, e.Topic);

            string mainsString = JsonSerializer.Serialize(StorageHoist);


            if (result.IsSuccess == true && !String.IsNullOrEmpty(publishTopic))
            {
                await _hiveMQService.PublishServiceAsync(publishTopic, mainsString);
            }
            else if (String.IsNullOrEmpty(publishTopic)) //In neutraal zetten we de publishTopic op null
            {
                Console.WriteLine("IN NEUTRAL MODE");
            }
            else
            {
                Console.WriteLine(result.Errors.First());
            }

        }

        public BaseResultModel ChangeMainProperties(Hoist hoistMessage, string topic)
        {
            if (hoistMessage != null) 
            {

                switch (topic)
                {

                    case HoistRoutes.SubscribeUp:
                        StorageHoist.Increment += hoistMessage.Increment;
                        StorageHoist.Length -= StorageHoist.Increment;
                        StorageHoist.HoistMovement = hoistMessage.HoistMovement;
                        publishTopic = HoistRoutes.PublishLocation;
                        return new BaseResultModel { IsSuccess = true };


                    case HoistRoutes.SubscribeDown:
                        StorageHoist.Increment += hoistMessage.Increment;
                        StorageHoist.Length += StorageHoist.Increment;
                        StorageHoist.HoistMovement = hoistMessage.HoistMovement;
                        publishTopic = HoistRoutes.PublishLocation;
                        return new BaseResultModel { IsSuccess = true };

                    case HoistRoutes.SubscribeNeutral:
                        StorageHoist.HoistMovement = hoistMessage.HoistMovement;
                        StorageHoist.Increment = 0;
                        publishTopic = "";
                        return new BaseResultModel { IsSuccess = true };

                    default:
                        var list = new List<string> { $"{topic} is not recognized" };
                        return new BaseResultModel { IsSuccess = false, Errors = list };
                }
            }
            else
            {
                var list = new List<string> { "Could not serialize received Hoist object" };
                return new BaseResultModel { IsSuccess = false, Errors = list };
            }
        }
    }
}
