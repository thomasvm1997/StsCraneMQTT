using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Models.CustomEventArgs;
using Wpe.SharkCrane.Core.Services.GantryService.GantryRoute;
using Wpe.SharkCrane.Core.Services.GantryService.Interfaces;
using Wpe.SharkCrane.Core.Services.HiveService.Interfaces;
using Wpe.SharkCrane.Core.Services.SpreaderService.SpreaderRoute;

namespace Wpe.SharkCrane.Core.Services.GantryService
{
    public class GantryService : IGantryService
    {
        public Gantry MainGantry { get; }
        private readonly IHiveMQService _hiveMQService;
        private string publishTopic;
        public GantryService(IHiveMQService hiveMQService)
        {
            _hiveMQService = hiveMQService;
            _hiveMQService.MessageReceived += OnMessageReceived;
            MainGantry = new Gantry { Distance = 4d };
        }

        private async void OnMessageReceived(object sender, CustomMessageReceivedEventArgs e)
        {

            Console.WriteLine($"HoistService received message on topic {e.Topic} : {e.Payload}");

            Gantry gantryMessage = JsonSerializer.Deserialize<Gantry>(e.Payload);

            BaseResultModel result = ChangeMainProperties(gantryMessage, e.Topic);

            string mainsString = JsonSerializer.Serialize(MainGantry);


            if (result.IsSuccess == true)
            {
                await _hiveMQService.PublishServiceAsync(publishTopic, mainsString);
            }
            else
            {
                Console.WriteLine(result.Errors.First());
            }

        }
        public BaseResultModel ChangeMainProperties(Gantry gantryMessage, string topic)
        {
            if (gantryMessage != null)
            {

                switch (topic)
                {

                    case GantryRoutes.SubscribeRight:
                        MainGantry.Distance += gantryMessage.Increment;
                        publishTopic = GantryRoutes.PublishRight;
                        return new BaseResultModel { IsSuccess = true };

                    case GantryRoutes.SubscribeLeft:
                        MainGantry.Distance -= gantryMessage.Increment;
                        publishTopic = GantryRoutes.PublishLeft;
                        return new BaseResultModel { IsSuccess = true };

                    case GantryRoutes.SubscribeLock:
                        MainGantry.IsHandBrakeOn = gantryMessage.IsHandBrakeOn;
                        publishTopic = GantryRoutes.SubscribeLock;
                        return new BaseResultModel { IsSuccess = true };

                    case GantryRoutes.SubscribeRelease:
                        MainGantry.IsHandBrakeOn = gantryMessage.IsHandBrakeOn;
                        publishTopic = GantryRoutes.PublishRelease;
                        return new BaseResultModel { IsSuccess = true };

                    default:
                        var list = new List<string> { $"{topic} is not recognized" };
                        return new BaseResultModel { IsSuccess = false, Errors = list };
                }
            }
            else
            {
                var list = new List<string> { "Could not serialize received Spreader Object" };
                return new BaseResultModel { IsSuccess = false, Errors = list };
            }
        }
    }
}
