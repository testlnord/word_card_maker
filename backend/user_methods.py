class User(object):
    def __init__(self, id: int, username: str, password: str):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id
