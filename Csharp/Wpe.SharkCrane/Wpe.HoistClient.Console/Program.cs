using Microsoft.Extensions.DependencyInjection;
using System.Text.Json;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Services.HiveService;
using Wpe.SharkCrane.Core.Services.HiveService.Interfaces;
using Wpe.SharkCrane.Core.Services.HoistService;
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

await hiveClient.SubscribeAsync("/hub/hoist");


var hoist = new Hoist { Increment = -1d };
var hoistString = JsonSerializer.Serialize(hoist); // Mock spreader info van hub => DEZE CODE NIET NODIG IN VOLLEDIG PROGRAMMA
while (true)
{
    Console.WriteLine("listening");

    await hiveClient.PublishAsync("/hub/hoist", hoistString); //mocken om data te verkijgen van hub => DEZE CODE NIET NODIG IN VOLLEDIG PROGRAMMA
                                                                    //We doen alsof we een message krijgen.
    await Task.Delay(1000);

}