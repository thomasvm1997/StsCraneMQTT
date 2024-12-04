using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Wpe.SharkCrane.Core.Services.HoistService.HoistRoutes
{
    public static class SpreaderRoutes
    {
        #region Subscribe
        public const string BaseSubscribe = "/hub/spreader";
        public const string SubscribeWiden = BaseSubscribe + "/widen";
        public const string SubscribeNarrow = BaseSubscribe + "/narrow";
        public const string SubscribeLock = BaseSubscribe + "/lock";
        public const string SubscribeUnlock = BaseSubscribe + "/unlock";

        #endregion

        #region Publish
        public const string BasePublish = "/spreader";
        public const string PublishWiden = BasePublish + "/widen";
        public const string PublishNarrow = BasePublish + "/narrow";
        public const string PublishLock = BaseSubscribe + "/lock";
        public const string PublishUnlock = BaseSubscribe + "/unlock";
        #endregion

    }
}
