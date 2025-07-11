from typing import Optional


def handle_command(line: str, cli) -> Optional[str]:
    """Handle special commands starting with '#'.

    Returns message if handled, None otherwise.
    """
    if not line.strip().startswith('#'):
        return None
    cmd = line.strip()[1:].strip()

    if cmd.startswith('start multi-turn'):
        cli.prompt.multi_turn = True
        return 'multi-turn on'
    if cmd.startswith('stop multi-turn'):
        cli.prompt.multi_turn = False
        cli.prompt.clear()
        return 'multi-turn off'
    if cmd.startswith('clear context'):
        cli.prompt.clear()
        return 'context cleared'
    if cmd.startswith('load context'):
        parts = cmd.split(maxsplit=2)
        if len(parts) == 3:
            cli.prompt.load(parts[2])
            return 'context loaded'
        return 'missing filename'
    if cmd.startswith('save context'):
        parts = cmd.split(maxsplit=2)
        name = parts[2] if len(parts) == 3 else 'context.txt'
        cli.prompt.save(name)
        return f'saved to {name}'
    if cmd.startswith('set model'):
        parts = cmd.split()
        if len(parts) == 3:
            cli.model = parts[2]
            return f'model set to {cli.model}'
    if cmd.startswith('set temperature'):
        parts = cmd.split()
        if len(parts) == 3:
            cli.temperature = float(parts[2])
            return f'temperature set to {cli.temperature}'
    if cmd.startswith('show config'):
        return f'model={cli.model} temp={cli.temperature} multi_turn={cli.prompt.multi_turn}'

    return 'unknown command'
