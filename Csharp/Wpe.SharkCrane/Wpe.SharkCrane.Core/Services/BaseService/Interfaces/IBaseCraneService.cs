using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Models;

namespace Wpe.SharkCrane.Core.Services.BaseService.Interfaces
{
    public interface IBaseCraneService<T> where T : BaseCraneObject
    {
        public BaseResultModel ChangeMainProperties(T objectMessage, string topic);
    }
}
