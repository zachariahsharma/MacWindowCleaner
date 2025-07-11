from codex_cli.cli import CodexCLI
from codex_cli.commands import handle_command


def test_start_stop_multi_turn():
    cli = CodexCLI()
    msg = handle_command('# start multi-turn', cli)
    assert msg == 'multi-turn on'
    assert cli.prompt.multi_turn is True
    msg = handle_command('# stop multi-turn', cli)
    assert msg == 'multi-turn off'
    assert cli.prompt.multi_turn is False


def test_set_model_and_temp():
    cli = CodexCLI()
    handle_command('# set model test-model', cli)
    assert cli.model == 'test-model'
    handle_command('# set temperature 0.5', cli)
    assert cli.temperature == 0.5
