using Microsoft.Extensions.DependencyInjection;
using Wpe.SharkCrane.Core.Services.HiveService;
using Wpe.SharkCrane.Core.Services.HiveService.Interfaces;
using Wpe.SharkCrane.Core.Services.SpreaderService.Interfaces;
using Wpe.SharkCrane.Core.Services.TrolleyService;
using Wpe.SharkCrane.Core.Services.TrolleyService.Interfaces;
using Wpe.SharkCrane.Core.Services.TrolleyService.TrolleyRoute;

#region injections

var serviceProvider = new ServiceCollection()
            .AddSingleton<IHiveMQService, HiveMQService>()
            .AddSingleton<ITrolleyService, TrolleyService>().BuildServiceProvider();


var hiveClient = serviceProvider.GetRequiredService<IHiveMQService>();
var spreaderService = serviceProvider.GetRequiredService<ISpreaderService>();
await hiveClient.ConnectAsync();
#endregion

Console.WriteLine("Hello, World!");

await hiveClient.SubscribeServiceAsync(TrolleyRoutes.BaseSubscribeWildcard);


while (true)
{

}
