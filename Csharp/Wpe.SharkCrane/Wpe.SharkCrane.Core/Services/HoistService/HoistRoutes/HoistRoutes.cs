using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Wpe.SharkCrane.Core.Services.HoistService.HoistRoutes
{
    public static class HoistRoutes
    {
        #region Subscribe
        public const string BaseSubscribe = "/hub/hoist";
        public const string SubscribeUp = BaseSubscribe + "/up";
        public const string SubscribeDown = BaseSubscribe + "/down";

        #endregion
        #region Publish
        public const string BasePublish = "/hoist";
        public const string PublishUp = BasePublish + "/up";
        public const string PublishDown = BasePublish + "/down";
        #endregion

    }
}
