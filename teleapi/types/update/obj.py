from .model import UpdateModel


class Update(UpdateModel):
    def __eq__(self, other) -> bool:
        return isinstance(other, Update) and other.id == self.id
