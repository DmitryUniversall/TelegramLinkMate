class FieldMixin:
    def __init__(self, *args, **kwargs) -> None:
        self.__attribute_name__ = None
        self.__owner__ = None

        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} [{f'{self.__attribute_name__} of {self.__owner__.__name__}' if self.__attribute_name__ else 'HAS_NO_OWNER'}]>"

    def __set_name__(self, owner: type, name: str) -> None:
        self.__attribute_name__ = name
        self.__owner__ = owner
