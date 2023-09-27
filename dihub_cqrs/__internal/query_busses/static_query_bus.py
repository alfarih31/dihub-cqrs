from dihub_cqrs.types import IStaticQueryBus, IQueryBus, TQuery, TQueryResult


class StaticQueryBus(IStaticQueryBus[TQuery, TQueryResult]):
    __parent_query_bus: IQueryBus

    def __init__(self, parent_query_bus: IQueryBus):
        self.__parent_query_bus = parent_query_bus

    async def query(self, query: TQuery) -> TQueryResult:
        return await self.__parent_query_bus.query(query)
