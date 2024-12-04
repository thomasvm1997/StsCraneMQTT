using Microsoft.Extensions.DependencyInjection;
using System.Text.Json;
using Wpe.SharkCrane.Core.Models;
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


var hoist = new Hoist { Increment = 1d };
var hoistString = JsonSerializer.Serialize(hoist); // Mock spreader info van hub => DEZE CODE NIET NODIG IN VOLLEDIG PROGRAMMA
while (true)
{
    Console.WriteLine("listening");

                                                                        
    await hiveClient.PublishServiceAsync("/hub/hoist/up", hoistString);                                                                    

    //We doen alsof we een message krijgen.
    await Task.Delay(1000);

}