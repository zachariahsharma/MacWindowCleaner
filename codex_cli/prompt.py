import os
from pathlib import Path

class Prompt:
    """Simple prompt context management."""
    def __init__(self, path: str = "current_context.txt"):
        self.path = Path(path)
        self.multi_turn = False
        self.path.write_text("")  # ensure file exists

    def clear(self):
        self.path.write_text("")

    def add_interaction(self, user: str, response: str):
        if not self.multi_turn:
            return
        with self.path.open("a") as f:
            f.write(user.rstrip() + "\n")
            f.write(response.rstrip() + "\n")

    def get_context(self) -> str:
        if not self.multi_turn:
            return ""
        return self.path.read_text()

    def get_messages(self):
        if not self.multi_turn:
            return []
        lines = self.path.read_text().splitlines()
        messages = []
        for i in range(0, len(lines), 2):
            user = lines[i]
            messages.append({"role": "user", "content": user})
            if i + 1 < len(lines):
                assistant = lines[i + 1]
                messages.append({"role": "assistant", "content": assistant})
        return messages

    def load(self, filename: str):
        src = Path(filename)
        if src.exists():
            self.path.write_text(src.read_text())
        else:
            raise FileNotFoundError(filename)

    def save(self, filename: str):
        dst = Path(filename)
        dst.write_text(self.path.read_text())
