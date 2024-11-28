using HiveMQtt.Client;
using HiveMQtt.Client.Options;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using Wpe.SharkCrane.Core.Services;
using Wpe.SharkCrane.Core.Services.Interfaces;

#region injections
var serviceProvider = new ServiceCollection()
            .AddSingleton<IHiveMQService, HiveMQService>()
            .AddSingleton<ISpreaderService, SpreaderService>().BuildServiceProvider();
            

var spreaderService = serviceProvider.GetRequiredService<ISpreaderService>();
#endregion

Console.WriteLine("Hello, World!");


