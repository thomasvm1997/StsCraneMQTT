using HiveMQtt.Client;
using HiveMQtt.Client.Options;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using System.Text.Json;
using System.Text.Json.Nodes;
using Wpe.SharkCrane.Core.Models;
using Wpe.SharkCrane.Core.Models.Enums;
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


var spreaderOpen = new Spreader { SpreaderMovement = SpreaderMovement.Open};
var spreaderNeutral = new Spreader { SpreaderMovement = SpreaderMovement.Neutral};
var spreaderClose = new Spreader {SpreaderMovement = SpreaderMovement.Close };
var spreaderOpentring = JsonSerializer.Serialize(spreaderOpen); // Mock spreader info van hub => DEZE CODE NIET NODIG IN VOLLEDIG PROGRAMMA
var spreaderNeutralString = JsonSerializer.Serialize(spreaderNeutral); // Mock spreader info van hub => DEZE CODE NIET NODIG IN VOLLEDIG PROGRAMMA
var spreaderCloseString = JsonSerializer.Serialize(spreaderClose); // Mock spreader info van hub => DEZE CODE NIET NODIG IN VOLLEDIG PROGRAMMA
int counter = 0;
while(true)
{
    Console.WriteLine("listening");
    
    if(counter < 5) 
    {
    await hiveClient.PublishServiceAsync("/hub/spreader/open", spreaderOpentring);
    }
    if(counter == 6)
    {
        await hiveClient.PublishServiceAsync("/hub/spreader/neutral", spreaderNeutralString);
    }
    if(counter == 6) {
    await hiveClient.PublishServiceAsync("/hub/spreader/close", spreaderCloseString);
    }

    counter++;
    await Task.Delay(1000);

}