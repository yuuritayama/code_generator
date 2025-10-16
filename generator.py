import random
import string

class CodeGenerator:
    def __init__(self, length: int, use_lowercase=True, use_uppercase=False, use_digits=False):
        self.length = length
        self.characters = ""
        if use_lowercase:
            self.characters += string.ascii_lowercase
        if use_uppercase:
            self.characters += string.ascii_uppercase
        if use_digits:
            self.characters += string.digits

        if not self.characters:
            raise ValueError("少なくとも1種類の文字を選択してください。")

    def generate_one(self) -> str:
        """1つのコードを生成する"""
        return ''.join(random.choices(self.characters, k=self.length))

    def generate_many(self, count: int) -> list[str]:
        """複数のコードを重複なしで生成する"""
        codes = set()
        while len(codes) < count:
            codes.add(self.generate_one())
        return list(codes)
