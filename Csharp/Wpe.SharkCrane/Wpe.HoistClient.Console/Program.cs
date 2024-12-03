using Microsoft.Extensions.DependencyInjection;

#region injections
var serviceProvider = new ServiceCollection()
            .AddSingleton<IHiveMQService, HiveMQService>()
            .AddSingleton<ISpreaderService, SpreaderService>().BuildServiceProvider();


var hiveClient = serviceProvider.GetRequiredService<IHiveMQService>();
var spreaderService = serviceProvider.GetRequiredService<ISpreaderService>();
await hiveClient.ConnectAsync();
#endregion

Console.WriteLine("blabla");