using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Wpe.SharkCrane.Core.Services.TrolleyService.TrolleyRoute
{
    public static class TrolleyRoutes
    {
        #region Subscribe
        public const string BaseSubscribe = "/hub/trolley";
        public const string BaseSubscribeWildcard = "/hub/trolley/#";
        public const string SubscribeUp = BaseSubscribe + "/forward";
        public const string SubscribeDown = BaseSubscribe + "/backward";
        public const string SubscribeNeutral = BaseSubscribe + "/neutral";

        #endregion
        #region Publish
        public const string BasePublish = "/trolley";
        public const string PublishLocation = BasePublish + "/location";
        #endregion
    }
}
