import os

from dotenv import load_dotenv

class Commander():
    def __init__(self):
        env_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
        load_dotenv(dotenv_path=env_path)

    def handle_command(self, message: str) -> str:
        p_msg = message.lower()

        if p_msg == '!help':
            return self.handle_help(p_msg)

        if p_msg == '!war':
            return self.handle_war(p_msg)

        if p_msg == '!promote':
            return self.handle_promote(p_msg)
        
        if p_msg == '!strike':
            return self.handle_strike(p_msg)

        if p_msg == '!update':
            return self.handle_update(p_msg)

    def handle_help(self, msg: str) -> str:
        return "`This is a help message that you can modify to show commands and help`"

    def handle_war(self, msg: str) -> str:
        return "`This will return the list of war participants`"

    def handle_promote(self, msg: str) -> str:
        return "`This will add a new user to the co-leader role`"

    def handle_strike(self, msg: str) -> str:
        return "`This will handle giving a strike to a clan mate`"

    def handle_update(self, msg: str) -> str:
        return "`This will update the clan with any new members`"