from src.error.base_error import CustomError


class CategoryNotExists(CustomError):
    """
    Категории слов с category_id не существует
    """
    def __init__(self, category_id: int):
        self.category_id = category_id
        self.message = f"Категория с id = {category_id} не существует!"
        super().__init__(self.message)


class CategoryNotExistsAdditionalInfo(CustomError):
    """
    Категории слов с category_id не существует
    """
    def __init__(self, category_id: int, user_id: int):
        self.category_id = category_id
        self.user_id = user_id
        self.message = f"Категория с id = {category_id} не существует! Операция над пользователем с id = {user_id} не была выполнена!"
        super().__init__(self.message)


class UserAlreadyBelongsCategory(CustomError):
    """
    Пользователь с user_id уже принадлежит к категории с category_id
    """
    def __init__(self, user_id: int, category_id: int):
        self.category_id = category_id
        self.user_id = user_id
        self.message = f"Ошибка добавления пользователя! Пользователь с id = {self.user_id} уже принадлежит к категории с id = {self.category_id}..."
        super().__init__(self.message)


class UserDoesNotBelongCategory(CustomError):
    """
    Пользователь с user_id не принадлежит к категории с category_id
    """
    def __init__(self, user_id: int, category_id: int):
        self.category_id = category_id
        self.user_id = user_id
        self.message = f"Ошибка удаления пользователя! Пользователь с id = {self.user_id} не состоит в списке участников категории с id = {self.category_id}..."
        super().__init__(self.message)
