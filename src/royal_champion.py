import discord
import os

from commands import Commander
from dotenv import load_dotenv

env_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

async def send_message(cmder, message, user_message):
    try:
        response = cmder.handle_command(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)

def run_royal_champion():
    intents = discord.Intents.all()
    intents.members = True

    client = discord.Client(intents=intents)
    cmder = Commander()

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.author.bot:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' on channel: '{channel}'")

        if user_message[0] == '!':
            await send_message(cmder, message, user_message)

    client.run(os.environ['DISCORD_TOKEN'])

if __name__ == "__main__":
    run_royal_champion()