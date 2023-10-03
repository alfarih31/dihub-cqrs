from dihub.decorators import module, configurable
from dihub.types import IConfigurableModule
from dihub_cqrs.__internal.dispatchers import Dispatcher
from dihub_cqrs.__internal.query_busses import QueryBus
from dihub_cqrs.types import CQRSOption


@configurable(config_type=CQRSOption)
@module(providers=[Dispatcher, QueryBus])
class CQRSModule(IConfigurableModule[CQRSOption]): ...
