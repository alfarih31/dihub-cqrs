from typing import Type, Dict, Annotated

from dihub.__internal.helpers import AnnotationOf
from dihub.constants import ROOT_MODULE_DELEGATE
from dihub.decorators import provider, inject, export
from dihub.types import IProviderRunner, IModuleDelegate, IProviderDelegate
from dihub_cqrs.__internal.helpers import get_command_name
from dihub_cqrs.constants import DISPATCHER, _COMMAND_HANDLER_ANNOTATIONS
from dihub_cqrs.exceptions import DuplicateCommandHandler, CommandHandlerNotFound
from dihub_cqrs.types import IDispatcher, IStaticDispatcher, TCommand, TCommandResult, ICommandHandler, CommandHandlerAnnotation
from .static_dispatcher import StaticDispatcher


@export
@provider(token=DISPATCHER)
class Dispatcher(IDispatcher, IProviderRunner):
    root_module_delegate: Annotated[IModuleDelegate, inject(ROOT_MODULE_DELEGATE)]
    command_handler_map: Dict[str, ICommandHandler]

    def __init__(self):
        self.command_handler_map = {}

    def find_command_handler_providers(self, providers: IProviderDelegate):
        # Resolve all providers that is a command handler
        for p, _ in providers:
            released_provider = p.release()
            command_handler_annotation = AnnotationOf(released_provider).get(_COMMAND_HANDLER_ANNOTATIONS, CommandHandlerAnnotation)
            if command_handler_annotation is not None:
                if command_handler_annotation.command_name in self.command_handler_map:
                    raise DuplicateCommandHandler(command_handler_annotation.command_name)
                else:
                    self.command_handler_map[command_handler_annotation.command_name] = released_provider

    def find_command_handler_providers_from_module(self, module: IModuleDelegate):
        self.find_command_handler_providers(module.providers)

        for m in module.imports:
            self.find_command_handler_providers(m.providers)

    def after_started(self):
        self.find_command_handler_providers_from_module(self.root_module_delegate)

    def create_static_dispatcher(self, t_command: Type[TCommand], t_result: Type[TCommandResult]) -> IStaticDispatcher[TCommand, TCommandResult]:
        return StaticDispatcher(self)

    async def dispatch(self, command: TCommand) -> TCommandResult:
        command_name = get_command_name(command)
        if command_name in self.command_handler_map:
            return await self.command_handler_map[command_name].handle(command)

        raise CommandHandlerNotFound(command_name)
