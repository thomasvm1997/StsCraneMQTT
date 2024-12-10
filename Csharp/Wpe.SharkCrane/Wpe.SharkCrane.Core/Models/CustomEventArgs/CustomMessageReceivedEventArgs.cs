using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Wpe.SharkCrane.Core.Models.CustomEventArgs
{
    public class CustomMessageReceivedEventArgs : EventArgs
    {
        public string Payload {  get; set; }
        public string Topic { get; set; }

        public CustomMessageReceivedEventArgs(string payload, string topic)
        {
            Payload = payload;
            Topic = topic;
        }
    }
}
