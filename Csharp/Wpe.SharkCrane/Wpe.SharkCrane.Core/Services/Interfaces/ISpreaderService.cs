using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models.CustomEventArgs;

namespace Wpe.SharkCrane.Core.Services.Interfaces
{
    public interface ISpreaderService
    {
        void OnMessageReceived(object sender, CustomMessageReceivedEventArgs e);
    }
}
