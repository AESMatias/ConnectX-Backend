# usuarios_conectados = {
#     "usuario1": {"writer": True, "reader": True, "jwt": "token123"},
#     "usuario2": {"writer": False, "reader": True, "jwt": "token456"},
#     # Otros usuarios...
# }


class User:
    def __init__(self, firtsMessage, reader, writer):
        self.xd = firtsMessage
        self.reader = reader
        self.writer = writer

    def user(self):
        jwt = self.xd
        print(jwt)

user = User("<NAME>", "<EMAIL>", "<EMAIL>")
user.user()

