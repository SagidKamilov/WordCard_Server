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

