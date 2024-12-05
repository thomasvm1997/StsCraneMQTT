using HiveMQtt.Client;
using HiveMQtt.Client.Options;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using System.Text.Json;
using System.Text.Json.Nodes;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Services.HiveService;
using Wpe.SharkCrane.Core.Services.HiveService.Interfaces;
using Wpe.SharkCrane.Core.Services.SpreaderService;
using Wpe.SharkCrane.Core.Services.SpreaderService.Interfaces;
using Wpe.SharkCrane.Core.Services.SpreaderService.SpreaderRoute;

#region injections
var serviceProvider = new ServiceCollection()
            .AddSingleton<IHiveMQService, HiveMQService>()
            .AddSingleton<ISpreaderService, SpreaderService>().BuildServiceProvider();


var hiveClient = serviceProvider.GetRequiredService<IHiveMQService>();
var spreaderService = serviceProvider.GetRequiredService<ISpreaderService>();
await hiveClient.ConnectAsync();
#endregion

Console.WriteLine("Hello, World!");

await hiveClient.SubscribeServiceAsync(SpreaderRoutes.BaseSubscribeWildcard);


var spreader = new Spreader { IsLocked = true, Increment = 1d };
var spreaderString = JsonSerializer.Serialize(spreader); // Mock spreader info van hub => DEZE CODE NIET NODIG IN VOLLEDIG PROGRAMMA
while(true)
{
    Console.WriteLine("listening");
    
     //mocken om data te verkijgen van hub => DEZE CODE NIET NODIG IN VOLLEDIG PROGRAMMA
    await hiveClient.PublishServiceAsync("/hub/spreader/lock", spreaderString);       
    await hiveClient.PublishServiceAsync("/hub/spreader/open", spreaderString);       
    //We doen alsof we een message krijgen.
    await Task.Delay(1000);

}