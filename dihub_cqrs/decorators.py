from typing import Type

from dihub.__internal.helpers import AnnotationOf
from dihub.decorators import provider
from dihub_cqrs.__internal.helpers import get_command_name, get_query_name
from dihub_cqrs.constants import _COMMAND_HANDLER_ANNOTATIONS, _QUERY_HANDLER_ANNOTATIONS
from dihub_cqrs.types import TCommand, TCommandHandler, CommandHandlerAnnotation, TQuery, TQueryResult, TQueryHandler, QueryHandlerAnnotation


def command_handler(command: Type[TCommand]):
    def wrapper(cls: TCommandHandler) -> TCommandHandler:
        AnnotationOf(cls).set(_COMMAND_HANDLER_ANNOTATIONS, CommandHandlerAnnotation(command_name=get_command_name(command)))
        return provider(cls)

    return wrapper


def query_handler(query: Type[TQuery], result: TQueryResult = None):
    def wrapper(cls: TQueryHandler) -> TQueryHandler:
        AnnotationOf(cls).set(_QUERY_HANDLER_ANNOTATIONS, QueryHandlerAnnotation(query_name=get_query_name(query), query_result=result))
        return provider(cls)

    return wrapper
