import discord
import yaml

from src.events_handler.on_member_join.banned_come_back import banned_come_back


class OnMemberJoin:

    @staticmethod
    async def handle(client: discord.Client, member: discord.Member):

        with open("run/config/config.yml", 'r') as stream:
            config = yaml.safe_load(stream)

        # Handle
        await banned_come_back(client, member, config)


