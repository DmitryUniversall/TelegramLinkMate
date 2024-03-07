from traceback import format_exception


def get_traceback_text(error: BaseException) -> str:
    return "".join(format_exception(type(error), error, error.__traceback__))
