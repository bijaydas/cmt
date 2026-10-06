from cmt.services.cache import Cache


class CommandService:
    def __init__(self):
        self.cache = Cache()

    def get_cache(self, plain_text_key: str):
        return self.cache.get(plain_text_key)

    def set_cache(self, plain_text_key: str, value):
        self.cache.set(plain_text_key, value)
