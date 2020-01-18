from datetime import datetime
from typing import Callable


class SingleValueCache:
    def __init__(self, expireAfterWrite: int, supplier: Callable[[], str]) -> None:
        self.expireAfterWrite = expireAfterWrite
        self.supplier = supplier
        self._createdAt = 0
        self._value = None

    def get(self):
        if (datetime.now().timestamp() - self._createdAt > self.expireAfterWrite * 1000):
            self._value = self.supplier()
            self._createdAt = datetime.now().timestamp()

        return self._value
