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
        public Gantry StorageGantry { get; }
        private readonly IHiveMQService _hiveMQService;
        private string publishTopic;
        public GantryService(IHiveMQService hiveMQService)
        {
            _hiveMQService = hiveMQService;
            _hiveMQService.MessageReceived += OnMessageReceived;
            StorageGantry = new Gantry { };
        }

        private async void OnMessageReceived(object sender, CustomMessageReceivedEventArgs e)
        {

            Console.WriteLine($"HoistService received message on topic {e.Topic} : {e.Payload}");

            Gantry gantryMessage = JsonSerializer.Deserialize<Gantry>(e.Payload);

            BaseResultModel result = ChangeMainProperties(gantryMessage, e.Topic);

            string mainsString = JsonSerializer.Serialize(StorageGantry);


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
                        StorageGantry.Increment += gantryMessage.Increment;
                        StorageGantry.Distance += StorageGantry.Distance;
                        StorageGantry.GantryMovement = gantryMessage.GantryMovement;
                        publishTopic = GantryRoutes.PublishLocation;
                        return new BaseResultModel { IsSuccess = true };

                    case GantryRoutes.SubscribeLeft:
                        StorageGantry.Increment += gantryMessage.Increment;
                        StorageGantry.Distance -= StorageGantry.Increment;
                        StorageGantry.GantryMovement = gantryMessage.GantryMovement;
                        publishTopic = GantryRoutes.PublishLocation;
                        return new BaseResultModel { IsSuccess = true };

                    case GantryRoutes.SubscribeLock:
                        StorageGantry.IsHandBrakeOn = gantryMessage.IsHandBrakeOn;
                        publishTopic = GantryRoutes.PublishLocked;
                        return new BaseResultModel { IsSuccess = true };

                    case GantryRoutes.SubscribeUnlock:
                        StorageGantry.IsHandBrakeOn = gantryMessage.IsHandBrakeOn;
                        publishTopic = GantryRoutes.PublishUnlocked;
                        return new BaseResultModel { IsSuccess = true };

                    case GantryRoutes.SubscribeNeutral:
                        StorageGantry.GantryMovement = gantryMessage.GantryMovement;
                        StorageGantry.Increment = 0;
                        publishTopic = "";
                        return new BaseResultModel { IsSuccess = true };

                    default:
                        var list = new List<string> { $"{topic} is not recognized" };
                        return new BaseResultModel { IsSuccess = false, Errors = list };
                }
            }
            else
            {
                var list = new List<string> { "Could not serialize received Gantry Object" };
                return new BaseResultModel { IsSuccess = false, Errors = list };
            }
        }
    }
}
