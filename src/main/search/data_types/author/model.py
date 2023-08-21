import teleapi


class AuthorModel(teleapi.orm.Model):
    name: str = teleapi.orm.StringModelField()
