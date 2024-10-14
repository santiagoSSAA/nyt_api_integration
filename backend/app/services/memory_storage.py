"""In-memory storage class module"""


class MemoryStorage:
    """In-memory storage Class"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MemoryStorage, cls).__new__(cls)
            cls._instance.storage = {}
        return cls._instance

    async def add_books(self, genre: str, books: list):
        self.storage[genre] = books

    def get_books(self, genre: str):
        return self.storage[genre]

    def get_all_genres(self):
        return list(self.storage.keys())

    def delete_genre(self, genre: str):
        if genre in self.storage:
            del self.storage[genre]
