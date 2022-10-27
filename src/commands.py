def handle_command(message: str) -> str:
    p_msg = message.lower()

    if p_msg == '!help':
        return "`This is a help message that you can modify to show commands and help`"