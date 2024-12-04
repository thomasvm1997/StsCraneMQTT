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
        private readonly IHiveMQService _hiveMQService;
        private readonly Spreader mainSpreader;
        private string publishTopic;
        public SpreaderService(IHiveMQService hiveMQService)
        {
            _hiveMQService = hiveMQService;
            _hiveMQService.MessageReceived += OnMessageReceived;
            mainSpreader = new Spreader();
        }

        public async void OnMessageReceived(object sender, CustomMessageReceivedEventArgs e)
        {
            Console.WriteLine($"HoistService received message on topic {e.Topic} : {e.Payload}");

            Spreader spreaderMessage = JsonSerializer.Deserialize<Spreader>(e.Payload);

            BaseResultModel result = ChangeMainProperties(spreaderMessage, e.Topic);

            string mainsString = JsonSerializer.Serialize(mainSpreader);


            if (result.IsSuccess == true)
            {
                await _hiveMQService.PublishServiceAsync(publishTopic, mainsString);
            }
            else
            {
                Console.WriteLine(result.Errors.First());
            }

        }

        private BaseResultModel ChangeMainProperties(Spreader spreaderMessage, string topic)
        {
            if (spreaderMessage != null)
            {

                switch (topic)
                {

                    case SpreaderRoutes.SubscribeWiden:
                        mainSpreader.Width += spreaderMessage.Increment;
                        publishTopic = SpreaderRoutes.PublishWiden;
                        return new BaseResultModel { IsSuccess = true };


                    case SpreaderRoutes.SubscribeNarrow:
                        mainSpreader.Width -= spreaderMessage.Increment;
                        publishTopic = SpreaderRoutes.PublishNarrow;
                        return new BaseResultModel { IsSuccess = true };
                    
                    case SpreaderRoutes.SubscribeLock:
                        mainSpreader.IsLocked = spreaderMessage.IsLocked;
                        publishTopic = SpreaderRoutes.PublishLock;
                        return new BaseResultModel { IsSuccess = true };

                    case SpreaderRoutes.SubscribeUnlock:
                        mainSpreader.IsLocked = spreaderMessage.IsLocked;
                        publishTopic = SpreaderRoutes.PublishUnlock;
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
