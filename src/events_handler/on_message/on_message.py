import discord
import yaml

# SETUP PART
from src.events_handler.on_message.setup.load_custom_commands import load_custom_commands
from src.events_handler.on_message.setup.load_roles import load_roles


class OnMessage:

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message):

        if message.guild == None or message.author.bot:
            return

        with open("run/config/config.yml", 'r') as stream:
            config = yaml.safe_load(stream)

        prefix = config['bot']['prefix']

        if not message.content or not message.content.startswith(prefix):
            return

        command = message.content.split(' ')[0][1:]
        args = message.content.split(' ')[1:]

        if command == 'load_roles':
            await load_roles(client, message, config)

        elif command == 'load_commands':
            await load_custom_commands(client, message, config)