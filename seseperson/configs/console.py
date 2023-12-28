from typing import Callable, Optional

from rich.console import Console as C


class Console(C):
    def __init__(self, console: C = C(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = console

    def info(self, content: str, *args, **kwargs):
        text = "[blue][¡][/blue] " + content
        self.console.print(text, *args, **kwargs)

    def success(self, content: str, *args, **kwargs):
        text = "[green][√][/green] " + content
        self.console.print(text, *args, **kwargs)

    def warn(self, content: str, *args, **kwargs):
        text = "[yellow][!][/yellow] " + content
        self.console.print(text, *args, **kwargs)

    def error(self, content: str, *args, **kwargs):
        text = "[red][×][/red] " + content
        self.console.print(text, *args, **kwargs)

    def get(
            self,
            prompt: str,
            default: str = "",
            assign_type: Optional[Callable] = None,
            reject_message: str = "",
            *args,
            **kwargs,
    ) -> str:
        self.console.print(f"[gray][?][/gray] [white]{prompt}[/white]")
        while True:
            text = self.console.input("> ", *args, **kwargs)
            if not text:
                self.info(f"已使用默认设置: {default if default else '空'}")
                return default

            if not assign_type:
                return text

            try:
                return assign_type(text)
            except Exception as e:
                self.warn(str(e))
                self.warn(reject_message)
