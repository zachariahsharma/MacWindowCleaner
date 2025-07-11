import openai

from .prompt import Prompt
from .commands import handle_command


class CodexCLI:
    def __init__(self, model: str = 'codex-mini-latest', temperature: float = 0.0, max_tokens: int = 512):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.prompt = Prompt()

    def query(self, text: str) -> str:
        messages = self.prompt.get_messages()
        messages.append({"role": "user", "content": text})
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return resp["choices"][0]["message"]["content"]

    def interact(self, line: str):
        cmd_result = handle_command(line, self)
        if cmd_result is not None:
            return cmd_result
        response = self.query(line)
        if self.prompt.multi_turn:
            self.prompt.add_interaction(line, response)
        return response


def main():
    cli = CodexCLI()
    print("Codex CLI (python) - type '# help' for commands")
    try:
        while True:
            line = input('> ')
            out = cli.interact(line)
            print(out)
    except (KeyboardInterrupt, EOFError):
        print()
        return


if __name__ == '__main__':
    main()
