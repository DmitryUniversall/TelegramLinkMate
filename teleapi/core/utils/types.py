class UNDEFINED:
    def __bool__(self) -> bool:
        return False

    def __str__(self) -> str:
        return self.__class__.__name__
