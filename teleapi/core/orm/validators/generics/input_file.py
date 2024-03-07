from .sized import SizedValidator


class InputFileValidator(SizedValidator):
    size_papping = {
        "mb": 1024 * 1024,
        "kb": 1024
    }

    def __init__(self, min_size: str = None, max_size: str = None, **kwargs) -> None:
        super().__init__(
            **kwargs,
            min_size=(int(min_size[:-2]) * self.__class__.size_papping.get(min_size[-2:].lower(), 1)) if min_size is not None else None,
            max_size=(int(max_size[:-2]) * self.__class__.size_papping.get(max_size[-2:].lower(), 1)) if max_size is not None else None
        )
