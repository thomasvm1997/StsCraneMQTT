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

namespace Wpe.SharkCrane.Core.Services.HoistService
{
    public class HoistService : IHoistService
    {
        private readonly IHiveMQService _hiveMQService;
        private readonly Hoist mainHoist;
        private string publishTopic;
        public HoistService(IHiveMQService hiveMQService)
        {
            _hiveMQService = hiveMQService;
            _hiveMQService.MessageReceived += OnMessageReceived;
            mainHoist = new Hoist { Length = 4d};
        }

        private async void OnMessageReceived(object sender, CustomMessageReceivedEventArgs e)
        {
            
            Console.WriteLine($"HoistService received message on topic {e.Topic} : {e.Payload}");

            Hoist hoistMessage = JsonSerializer.Deserialize<Hoist>(e.Payload);

            BaseResultModel result = ChangeMainProperties(hoistMessage, e.Topic);

            string mainsString = JsonSerializer.Serialize(mainHoist);
           

            if(result.IsSuccess == true)
            {
                await _hiveMQService.PublishServiceAsync(publishTopic, mainsString);
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
                        mainHoist.Length -= hoistMessage.Increment;
                        publishTopic = HoistRoutes.PublishUp;
                        return new BaseResultModel { IsSuccess = true };


                    case HoistRoutes.SubscribeDown:
                        mainHoist.Length += hoistMessage.Increment;
                        publishTopic = HoistRoutes.PublishDown;
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
