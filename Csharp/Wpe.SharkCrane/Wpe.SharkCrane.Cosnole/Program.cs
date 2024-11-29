using HiveMQtt.Client;
using HiveMQtt.Client.Options;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using System.Text.Json;
using System.Text.Json.Nodes;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Services;
using Wpe.SharkCrane.Core.Services.Interfaces;

#region injections
var serviceProvider = new ServiceCollection()
            .AddSingleton<IHiveMQService, HiveMQService>()
            .AddSingleton<ISpreaderService, SpreaderService>().BuildServiceProvider();


var hiveClient = serviceProvider.GetRequiredService<IHiveMQService>();
var spreaderService = serviceProvider.GetRequiredService<ISpreaderService>();
await hiveClient.ConnectAsync();
#endregion

Console.WriteLine("Hello, World!");

await hiveClient.SubscribeAsync("/hub/spreader");


var spreader = new Spreader { IsLocked = true, Width = 1m };
var spreaderString = JsonSerializer.Serialize(spreader); // Mock spreader info van hub
while(true)
{
    await Task.Delay(1000);
    await hiveClient.PublishAsync("/hub/spreader", spreaderString); //mocken om data te verkijgen van hub
                                                                    //We doen alsof we een message krijgen.
    Console.WriteLine("listening");
}