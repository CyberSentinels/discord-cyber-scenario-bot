class AsyncIterableList():
    def __init__(self, items):
        self.current = 0
        self.n = len(items)
        self.items = items

    def __aiter__(self):
        return self

    async def __anext__(self):
        self.current += 1

        if self.current > self.n:
            raise StopAsyncIteration

        return self.items[self.current - 1]
