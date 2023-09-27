from typing import Any

from dihub_cqrs.types import TQueryResult


class DuplicateCommandHandler(RuntimeError):
    def __init__(self, command_name: str):
        super().__init__("Duplicate command handler for command '%s'" % command_name)


class DuplicateQueryHandler(RuntimeError):
    def __init__(self, query_name: str):
        super().__init__("Duplicate query handler for query '%s'" % query_name)


class CommandHandlerNotFound(RuntimeError):
    def __init__(self, command_name: str):
        super().__init__("No handler found for command '%s'" % command_name)


class QueryHandlerNotFound(RuntimeError):
    def __init__(self, query_name: str):
        super().__init__("No handler found for query '%s'" % query_name)


class InvalidQueryResult(RuntimeError):
    def __init__(self, actual_type: Any, expected_type: TQueryResult):
        super().__init__("Expected result type: '%s', Got: '%s'" % (expected_type.__name__, actual_type.__class__.__name__))
