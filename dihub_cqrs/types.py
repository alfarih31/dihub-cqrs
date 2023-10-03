from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Protocol, TypeVar, Type

TCommand = TypeVar("TCommand", covariant=True, bound=type)
TCommandResult = TypeVar("TCommandResult", covariant=True)

TQuery = TypeVar("TQuery", covariant=True, bound=type)
TQueryResult = TypeVar("TQueryResult", covariant=True)


class ICommandHandler(Protocol[TCommand, TCommandResult]):
    @abstractmethod
    async def handle(self, command: TCommand) -> TCommandResult: ...


TCommandHandler = TypeVar("TCommandHandler", covariant=True, bound=ICommandHandler)


@dataclass(frozen=True)
class CommandHandlerAnnotation:
    command_name: str


class IStaticDispatcher(Protocol[TCommand, TCommandResult]):
    @abstractmethod
    async def dispatch(self, command: TCommand) -> TCommandResult: ...


class IDispatcher(ABC):
    @abstractmethod
    def create_static_dispatcher(self, t_command: Type[TCommand], t_result: Type[TCommandResult]) -> IStaticDispatcher[TCommand, TCommandResult]: ...

    @abstractmethod
    async def dispatch(self, command: TCommand) -> TCommandResult: ...


@dataclass(frozen=True)
class CQRSOption: ...


@dataclass(frozen=True)
class QueryHandlerAnnotation:
    query_name: str
    query_result: TQueryResult


class IQueryHandler(Protocol[TQuery, TQueryResult]):
    @abstractmethod
    async def handle(self, query: TQuery) -> TQueryResult: ...


TQueryHandler = TypeVar("TQueryHandler", covariant=True, bound=IQueryHandler)


class IStaticQueryBus(Protocol[TQuery, TQueryResult]):
    @abstractmethod
    async def query(self, query: TQuery) -> TQueryResult: ...


class IQueryBus(ABC):
    @abstractmethod
    def create_static_query_bus(self, t_query: Type[TQuery], t_result: Type[TQueryResult]) -> IStaticQueryBus[TQuery, TQueryResult]: ...

    @abstractmethod
    async def query(self, query: TQuery) -> TQueryResult: ...
