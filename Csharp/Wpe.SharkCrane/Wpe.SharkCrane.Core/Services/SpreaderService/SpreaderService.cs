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
using Wpe.SharkCrane.Core.Services.HoistService.HoistRoute;
using Wpe.SharkCrane.Core.Services.SpreaderService.Interfaces;
using Wpe.SharkCrane.Core.Services.SpreaderService.SpreaderRoute;

namespace Wpe.SharkCrane.Core.Services.SpreaderService
{
    public class SpreaderService : ISpreaderService
    {
        public Spreader StorageSpreader { get;}
        private readonly IHiveMQService _hiveMQService;
        private string publishTopic;

        public SpreaderService(IHiveMQService hiveMQService)
        {
            _hiveMQService = hiveMQService;
            _hiveMQService.MessageReceived += OnMessageReceived;
            StorageSpreader = new Spreader {};
        }

        private async void OnMessageReceived(object sender, CustomMessageReceivedEventArgs e)
        {
            Console.WriteLine($"HoistService received message on topic {e.Topic} : {e.Payload}");

            Spreader spreaderMessage = JsonSerializer.Deserialize<Spreader>(e.Payload);
 
            BaseResultModel result = ChangeMainProperties(spreaderMessage, e.Topic);

            string mainsString = JsonSerializer.Serialize(StorageSpreader);


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

        public BaseResultModel ChangeMainProperties(Spreader spreaderMessage, string topic)
        {
            if (spreaderMessage != null)
            {

                switch (topic)
                {

                    case SpreaderRoutes.SubscribeOpen:
                        StorageSpreader.Increment += spreaderMessage.Increment;
                        StorageSpreader.Width += StorageSpreader.Increment;
                        StorageSpreader.SpreaderMovement = spreaderMessage.SpreaderMovement;
                        publishTopic = SpreaderRoutes.PublishWidth;
                        return new BaseResultModel { IsSuccess = true };


                    case SpreaderRoutes.SubscribeClose:
                        StorageSpreader.Increment += spreaderMessage.Increment;
                        StorageSpreader.Width -= StorageSpreader.Increment;
                        StorageSpreader.SpreaderMovement = spreaderMessage.SpreaderMovement;
                        publishTopic = SpreaderRoutes.PublishWidth;
                        return new BaseResultModel { IsSuccess = true };
                    
                    case SpreaderRoutes.SubscribeLock:
                        StorageSpreader.IsLocked = spreaderMessage.IsLocked;
                        publishTopic = SpreaderRoutes.PublishLock;
                        return new BaseResultModel { IsSuccess = true };

                    case SpreaderRoutes.SubscribeUnlock:
                        StorageSpreader.IsLocked = spreaderMessage.IsLocked;
                        publishTopic = SpreaderRoutes.PublishUnlock;
                        return new BaseResultModel { IsSuccess = true };

                    case SpreaderRoutes.SubscribeNeutral:
                        StorageSpreader.SpreaderMovement = spreaderMessage.SpreaderMovement;
                        StorageSpreader.Increment = 0;
                        publishTopic = "";
                        return new BaseResultModel { IsSuccess = false };

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
