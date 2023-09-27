from dihub_cqrs.types import TCommand, TQuery


def get_command_name(command: TCommand) -> str:
    name = None
    if isinstance(command, type):
        name = str(command)
    else:
        name = str(command.__class__)
    return "<command %s>" % name


def get_query_name(query: TQuery) -> str:
    name = None
    if isinstance(query, type):
        name = str(query)
    else:
        name = str(query.__class__)
    return "<query %s>" % name
