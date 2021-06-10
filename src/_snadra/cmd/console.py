from rich.console import Console


class SnadraConsole:
    def __init__(self, config="") -> None:
        self._config = config
        self.__console = Console()

    def log(self, *args, **kwargs) -> None:
        self.__console.log(*args, **kwargs)

    def print(self, *args, **kwargs) -> None:
        self.__console.print(*args, **kwargs)

    def print_exception(self, *args, **kwargs) -> None:
        self.__console.print_exception(*args, **kwargs)
