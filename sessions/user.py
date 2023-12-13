

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

