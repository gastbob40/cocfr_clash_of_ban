import discord
import yaml

from src.events_handler.on_member_join.banned_come_back import banned_come_back
from src.events_handler.on_member_join.log_invite import log_invite


class OnMemberJoin:

    @staticmethod
    async def handle(client: discord.Client, member: discord.Member):

        with open("run/config/config.yml", 'r') as stream:
            config = yaml.safe_load(stream)

        # Check if the user is a banned member
        await banned_come_back(client, member, config)

        # Log Invite
        await log_invite(client, member, config)
