import discord
import yaml

from src.events_handler.on_reaction_add.forbidden_emoji import forbidden_emoji


class OnReactionAdd:

    @staticmethod
    async def handle(client: discord.Client, payload: discord.RawReactionActionEvent):

        if payload.emoji.name in ['💩', '🖕', '♿']:
            with open("run/config/config.yml", 'r') as stream:
                config = yaml.safe_load(stream)

            await forbidden_emoji(client, payload, config)
