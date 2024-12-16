using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Wpe.SharkCrane.Core.Services.GantryService.GantryRoute
{
    public static class GantryRoutes
    {
        #region Subscribe
        public const string BaseSubscribe = "/hub/gantry";
        public const string BaseSubscribeWildcard = "/hub/gantry/#";
        public const string SubscribeLeft = BaseSubscribe + "/left";
        public const string SubscribeRight = BaseSubscribe + "/right";
        public const string SubscribeNeutral = BaseSubscribe + "/neutral";
        public const string SubscribeLock = BaseSubscribe + "/handbrake/lock";
        public const string SubscribeUnlock = BaseSubscribe + "/handbrake/release";

        #endregion
        #region Publish
        public const string BasePublish = "/gantry";
        public const string PublishLocation = BasePublish + "/location";
        public const string PublishLocked = BasePublish + "/locked";
        public const string PublishUnlocked = BasePublish + "/unlocked";
        #endregion
    }
}
