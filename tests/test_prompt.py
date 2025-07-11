import tempfile
from pathlib import Path
from codex_cli.prompt import Prompt


def test_add_interaction_and_context():
    with tempfile.TemporaryDirectory() as tmp:
        pfile = Path(tmp)/"context.txt"
        prompt = Prompt(str(pfile))
        prompt.multi_turn = True
        prompt.add_interaction("hello", "world")
        ctx = prompt.get_context()
        assert "hello" in ctx and "world" in ctx
        msgs = prompt.get_messages()
        assert msgs == [
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": "world"},
        ]


def test_load_and_save():
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp)/"src.txt"
        dst = Path(tmp)/"dst.txt"
        src.write_text("line1\nline2\n")
        prompt = Prompt(str(Path(tmp)/"context.txt"))
        prompt.load(str(src))
        prompt.save(str(dst))
        assert dst.read_text() == "line1\nline2\n"
