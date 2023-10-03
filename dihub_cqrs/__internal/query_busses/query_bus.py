from typing import Type, Dict, Tuple, Annotated

from dihub.__internal.helpers import AnnotationOf
from dihub.constants import ROOT_MODULE_DELEGATE
from dihub.decorators import provider, inject, export
from dihub.types import IProviderRunner, IModuleDelegate, IProviderDelegate
from dihub_cqrs.__internal.helpers import get_query_name
from dihub_cqrs.constants import _QUERY_HANDLER_ANNOTATIONS, QUERY_BUS
from dihub_cqrs.exceptions import DuplicateQueryHandler, QueryHandlerNotFound, InvalidQueryResult
from dihub_cqrs.types import IQueryBus, IStaticQueryBus, TQuery, TQueryResult, IQueryHandler, QueryHandlerAnnotation
from .static_query_bus import StaticQueryBus


@export
@provider(token=QUERY_BUS)
class QueryBus(IQueryBus, IProviderRunner):
    root_module_delegate: Annotated[IModuleDelegate, inject(ROOT_MODULE_DELEGATE)]
    query_handler_map: Dict[str, Tuple[IQueryHandler, TQueryResult]]

    def __init__(self):
        self.query_handler_map = {}

    def find_query_handler_providers(self, providers: IProviderDelegate):
        # Resolve all providers that is a query handler
        for p, _ in providers:
            released_provider = p.release()
            query_handler_annotation = AnnotationOf(released_provider).get(_QUERY_HANDLER_ANNOTATIONS, QueryHandlerAnnotation)
            if query_handler_annotation is not None:
                if query_handler_annotation.query_name in self.query_handler_map:
                    raise DuplicateQueryHandler(query_handler_annotation.query_name)
                else:
                    self.query_handler_map[query_handler_annotation.query_name] = (released_provider, query_handler_annotation.query_result)

    def find_query_handler_providers_from_module(self, module: IModuleDelegate):
        self.find_query_handler_providers(module.providers)

        for m in module.imports:
            self.find_query_handler_providers(m.providers)

    def after_started(self):
        self.find_query_handler_providers_from_module(self.root_module_delegate)

    def create_static_query_bus(self, t_query: Type[TQuery], t_result: Type[TQueryResult]) -> IStaticQueryBus[TQuery, TQueryResult]:
        return StaticQueryBus(self)

    async def query(self, query: TQuery) -> TQueryResult:
        query_name = get_query_name(query)
        if query_name in self.query_handler_map:
            handler, result_type = self.query_handler_map[query_name]
            result = await handler.handle(query)
            if result_type is not None and not isinstance(result, result_type):
                raise InvalidQueryResult(result, result_type)

            return result

        raise QueryHandlerNotFound(query_name)
