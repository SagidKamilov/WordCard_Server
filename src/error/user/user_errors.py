from src.error.base_error import CustomError


class UserAlreadyExists(CustomError):
    """
    Если имя пользователя уже занято
    """
    def __init__(self, username: str):
        self.username = username
        self.message = f"Пользователь с именем {self.username} уже занят"
        super().__init__(self.message)


class UserIdNotExists(CustomError):
    """
    Если пользователь с передаваемым user_id не был найден
    """
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.message = f"Пользователь с id = `{self.user_id}` не существует!"
        super().__init__(self.message)


class UserUsernameNotExists(CustomError):
    """
    Если пользователь с передаваемым username не был найден
    """
    def __init__(self, username: str):
        self.username = username
        self.message = f"Пользователя с username `{self.username}` не существует!"
        super().__init__(self.message)


class UserWrongPassword(CustomError):
    """
    Введен неправильный пароль
    """
    def __init__(self):
        self.message = f"Неверный пароль! Повторите попытку"
        super().__init__(self.message)
