using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Wpe.SharkCrane.Core.Services.SpreaderService.SpreaderRoute
{
    public static class SpreaderRoutes
    {
        #region Subscribe
        public const string BaseSubscribe = "/hub/spreader";
        public const string BaseSubscribeWildcard = "/hub/spreader/#"; //Gebruiken we om naar alle topics te luisteren
        public const string SubscribeOpen = BaseSubscribe + "/open";
        public const string SubscribeClose = BaseSubscribe + "/close";
        public const string SubscribeLock = BaseSubscribe + "/lock";
        public const string SubscribeUnlock = BaseSubscribe + "/unlock";
        public const string SubscribeNeutral = BaseSubscribe + "/neutral";

        #endregion

        #region Publish
        public const string BasePublish = "/spreader";
        public const string PublishWidth = BasePublish + "/width";
        public const string PublishLock = BasePublish + "/lock";
        public const string PublishUnlock = BasePublish + "/unlock";
        #endregion

    }
}
