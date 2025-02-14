from aiogram.filters import Filter
from aiogram.types import Message


class CommandFilter(Filter):
    def __init__(self, argument: str):
        self.argument = argument

    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False

        # Extract command arguments
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return False

        args = parts[1]
        print(args)
        return args.startswith(self.argument)
