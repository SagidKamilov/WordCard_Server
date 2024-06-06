from passlib.context import CryptContext

from src.config.settings import HASHING_ALGORITHM


class HashGenerator:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=[HASHING_ALGORITHM], deprecated="auto")

    def generate_hash_from_password(self, password: str) -> str:
        hashed_password: str = self.pwd_context.hash(secret=password)
        return hashed_password

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(secret=password, hash=hashed_password)