#region injections
using Microsoft.Extensions.DependencyInjection;
using System.Text.Json;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Models.Enums;
using Wpe.SharkCrane.Core.Services.GantryService;
using Wpe.SharkCrane.Core.Services.GantryService.GantryRoute;
using Wpe.SharkCrane.Core.Services.GantryService.Interfaces;
using Wpe.SharkCrane.Core.Services.HiveService;
using Wpe.SharkCrane.Core.Services.HiveService.Interfaces;
using Wpe.SharkCrane.Core.Services.HoistService.HoistRoute;
using Wpe.SharkCrane.Core.Services.HoistService.Interfaces;

var serviceProvider = new ServiceCollection()
            .AddSingleton<IHiveMQService, HiveMQService>()
            .AddSingleton<IGantryService, GantryService>().BuildServiceProvider();


var hiveClient = serviceProvider.GetRequiredService<IHiveMQService>();
var gantryService = serviceProvider.GetRequiredService<IGantryService>();
await hiveClient.ConnectAsync();
#endregion

Console.WriteLine("Hello, World!");

await hiveClient.SubscribeServiceAsync(GantryRoutes.BaseSubscribeWildcard);


var gantryLeft = new Gantry { GantryMovement = GantryMovement.Left, Increment = 0.2d };
var gantryNeutral = new Gantry { GantryMovement = GantryMovement.Neutral, Increment = 0.2d }; //HUB MOET STANDAARD INCREMENT DOORGEVEN
var gantryRight = new Gantry { GantryMovement = GantryMovement.Right, Increment = 0.2d };
var gantryLeftString = JsonSerializer.Serialize(gantryLeft); // Mock spreader info van hub => DEZE CODE NIET NODIG IN VOLLEDIG PROGRAMMA
var gantryNeutralString = JsonSerializer.Serialize(gantryNeutral); // Mock spreader info van hub => DEZE CODE NIET NODIG IN VOLLEDIG PROGRAMMA
var gantryRightString = JsonSerializer.Serialize(gantryRight); // Mock spreader info van hub => DEZE CODE NIET NODIG IN VOLLEDIG PROGRAMMA
var counter = 0;
while (true)
{
    Console.WriteLine("listening");

    //if (counter <= 5)
    //{
    //    await hiveClient.PublishServiceAsync("/hub/gantry/right", gantryRightString);
    //}
    //if (counter == 6)
    //{
    //    await hiveClient.PublishServiceAsync("/hub/gantry/neutral", gantryNeutralString);
    //}
    //if (counter > 6)
    //{
    //    await hiveClient.PublishServiceAsync("/hub/gantry/left", gantryLeftString);
    //}

    //counter++;

    await Task.Delay(1000);

}
