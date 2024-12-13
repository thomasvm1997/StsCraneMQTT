using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Models.CustomEventArgs;
using Wpe.SharkCrane.Core.Services.HiveService.Interfaces;
using Wpe.SharkCrane.Core.Services.HoistService.HoistRoute;
using Wpe.SharkCrane.Core.Services.TrolleyService.Interfaces;
using Wpe.SharkCrane.Core.Services.TrolleyService.TrolleyRoute;

namespace Wpe.SharkCrane.Core.Services.TrolleyService
{
    public class TrolleyService : ITrolleyService
    {
        public Trolley StorageTrolley { get; }
        private readonly IHiveMQService _hiveMQService;
        private string publishTopic;
        public TrolleyService(IHiveMQService hiveMQService)
        {
            _hiveMQService = hiveMQService;
            _hiveMQService.MessageReceived += OnMessageReceived;
            StorageTrolley = new Trolley { };
        }

        private async void OnMessageReceived(object sender, CustomMessageReceivedEventArgs e)
        {

            Console.WriteLine($"HoistService received message on topic {e.Topic} : {e.Payload}");

            Trolley trolleyMessage = JsonSerializer.Deserialize<Trolley>(e.Payload);

            BaseResultModel result = ChangeMainProperties(trolleyMessage, e.Topic);

            string mainsString = JsonSerializer.Serialize(StorageTrolley);


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

        public BaseResultModel ChangeMainProperties(Trolley trolleyMessage, string topic)
        {
            if (trolleyMessage != null)
            {

                switch (topic)
                {

                    case TrolleyRoutes.SubscribeForward:
                        StorageTrolley.Increment += trolleyMessage.Increment;
                        StorageTrolley.Distance += StorageTrolley.Increment;
                        StorageTrolley.TrolleyMovement = trolleyMessage.TrolleyMovement;
                        publishTopic = TrolleyRoutes.PublishLocation;
                        return new BaseResultModel { IsSuccess = true };


                    case TrolleyRoutes.SubscribeBackward:
                        StorageTrolley.Increment += trolleyMessage.Increment;
                        StorageTrolley.Distance -= StorageTrolley.Increment;
                        StorageTrolley.TrolleyMovement = trolleyMessage.TrolleyMovement;
                        publishTopic = TrolleyRoutes.PublishLocation;
                        return new BaseResultModel { IsSuccess = true };

                    case TrolleyRoutes.SubscribeNeutral:
                        StorageTrolley.TrolleyMovement = trolleyMessage.TrolleyMovement;
                        StorageTrolley.Increment = 0;
                        publishTopic = "";
                        return new BaseResultModel { IsSuccess = true };

                    default:
                        var list = new List<string> { $"{topic} is not recognized" };
                        return new BaseResultModel { IsSuccess = false, Errors = list };
                }
            }
            else
            {
                var list = new List<string> { "Could not serialize received Trolley object" };
                return new BaseResultModel { IsSuccess = false, Errors = list };
            }
        }
    }
}
