using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wpe.SharkCrane.Core.Services.Interfaces;

namespace Wpe.SharkCrane.Core.Services
{
    public class SpreaderService : ISpreaderService
    {
        private readonly IHiveMQService _hiveMQService;

        public SpreaderService(IHiveMQService hiveMQService)
        {
            _hiveMQService = hiveMQService;
        }


    }
}
