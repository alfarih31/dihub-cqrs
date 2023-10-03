from asyncio import run
from dataclasses import dataclass
from inspect import iscoroutine

from dihub.decorators import module, root, for_root
from dihub.types import IRootRunner, IModuleDelegate
from dihub_cqrs import CQRSModule
from dihub_cqrs.constants import DISPATCHER
from dihub_cqrs.decorators import command_handler
from dihub_cqrs.types import ICommandHandler, IDispatcher


@dataclass(frozen=True)
class ACommand:
    prop: int


@dataclass(frozen=True)
class AResult:
    some: str


@command_handler(ACommand)
class CommandHandler(ICommandHandler[ACommand, AResult]):
    async def handle(self, arg: ACommand) -> AResult:
        return AResult(some="AUAH")


@root
@module(imports=[for_root(CQRSModule)], providers=[CommandHandler])
class RootModule(IRootRunner):
    async def after_started(self, root_module_delegate: IModuleDelegate):
        dispatcher = root_module_delegate[CQRSModule].providers[DISPATCHER][0].cast(IDispatcher)
        static_dispatcher = dispatcher.create_static_dispatcher(ACommand, AResult)

        res1 = await static_dispatcher.dispatch(ACommand(prop=2))
        res = await dispatcher.dispatch(ACommand(prop=1))

        print(res.some == res1.some, res, res1)


async def main():
    r = RootModule()
    if iscoroutine(r):
        await r


if __name__ == "__main__":
    run(main())
