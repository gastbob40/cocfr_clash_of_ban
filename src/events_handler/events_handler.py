import discord

from src.events_handler.on_member_join.on_member_join import OnMemberJoin
from src.events_handler.on_message.on_message import OnMessage


class EventsHandler:

    @staticmethod
    async def handle_on_message(client: discord.Client, message: discord.Message):
        await OnMessage.handle(client, message)

    @staticmethod
    def handle_on_ready(client: discord.Client):
        print('We have logged in as {0.user}'.format(client))

    @staticmethod
    async def handle_on_member_join(client: discord.Client, member: discord.Member):
        await OnMemberJoin.handle(client, member)
