using Microsoft.Extensions.DependencyInjection;
using System.Text.Json;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Models.Enums;
using Wpe.SharkCrane.Core.Services.HiveService;
using Wpe.SharkCrane.Core.Services.HiveService.Interfaces;
using Wpe.SharkCrane.Core.Services.HoistService;
using Wpe.SharkCrane.Core.Services.HoistService.HoistRoute;
using Wpe.SharkCrane.Core.Services.HoistService.Interfaces;


#region injections
var serviceProvider = new ServiceCollection()
            .AddSingleton<IHiveMQService, HiveMQService>()
            .AddSingleton<IHoistService, HoistService>().BuildServiceProvider();


var hiveClient = serviceProvider.GetRequiredService<IHiveMQService>();
var hoistService = serviceProvider.GetRequiredService<IHoistService>();
await hiveClient.ConnectAsync();
#endregion

Console.WriteLine("Hello, World!");

await hiveClient.SubscribeServiceAsync(HoistRoutes.BaseSubscribeWildcard);


var hoistUp = new Hoist { HoistMovement = HoistMovement.Up, Increment = 0.2d };
var hoistNeutral = new Hoist { HoistMovement = HoistMovement.Neutral, Increment = 0.2d }; //HUB MOET STANDAARD INCREMENT DOORGEVEN
var hoistDown = new Hoist { HoistMovement = HoistMovement.Down, Increment = 0.2d };
var hoistUptring = JsonSerializer.Serialize(hoistUp); // Mock spreader info van hub => DEZE CODE NIET NODIG IN VOLLEDIG PROGRAMMA
var hoistNeutralString = JsonSerializer.Serialize(hoistNeutral); // Mock spreader info van hub => DEZE CODE NIET NODIG IN VOLLEDIG PROGRAMMA
var hoistDownString = JsonSerializer.Serialize(hoistDown); // Mock spreader info van hub => DEZE CODE NIET NODIG IN VOLLEDIG PROGRAMMA
var counter = 0;
while (true)
{
    Console.WriteLine("listening");

    if (counter <= 4)
    {
        await hiveClient.PublishServiceAsync("/hub/hoist/down", hoistDownString);
    }
    if (counter == 6)
    {
        await hiveClient.PublishServiceAsync("/hub/hoist/neutral", hoistNeutralString);
    }
    if (counter >= 6)
    {
        await hiveClient.PublishServiceAsync("/hub/hoist/up", hoistUptring);
    }

    counter++;

    await Task.Delay(1000);

}