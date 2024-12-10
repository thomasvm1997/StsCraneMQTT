#region injections
using Microsoft.Extensions.DependencyInjection;
using System.Text.Json;
using Wpe.SharkCrane.Core.Models;
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


var gantry = new Gantry { Increment = 1d };
var gantryString = JsonSerializer.Serialize(gantry); // Mock spreader info van hub => DEZE CODE NIET NODIG IN VOLLEDIG PROGRAMMA
while (true)
{
    Console.WriteLine("listening");


    await hiveClient.PublishServiceAsync("/hub/gantry/right", gantryString);


    //We doen alsof we een message krijgen.
    await Task.Delay(1000);

}
