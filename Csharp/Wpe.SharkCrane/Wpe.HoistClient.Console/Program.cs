using Microsoft.Extensions.DependencyInjection;
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

