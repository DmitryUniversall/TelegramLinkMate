from .model import ContactModel


class Contact(ContactModel):
    def __eq__(self, other) -> bool:
        return isinstance(other, Contact) and other.phone_number == self.phone_number
