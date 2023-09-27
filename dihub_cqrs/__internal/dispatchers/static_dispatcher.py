from dihub_cqrs.types import IStaticDispatcher, IDispatcher, TCommand, TCommandResult


class StaticDispatcher(IStaticDispatcher[TCommand, TCommandResult]):
    __parent_dispatcher: IDispatcher

    def __init__(self, parent_dispatcher: IDispatcher):
        self.__parent_dispatcher = parent_dispatcher

    async def dispatch(self, command: TCommand) -> TCommandResult:
        return await self.__parent_dispatcher.dispatch(command)
