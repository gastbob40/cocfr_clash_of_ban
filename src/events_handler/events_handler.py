import discord

from src.events_handler.on_member_join.on_member_join import OnMemberJoin
from src.events_handler.on_message.on_message import OnMessage
from src.events_handler.on_message_delete.on_message_delete import OnMessageDelete
from src.events_handler.on_message_edit.on_message_edit import OnMessageEdit
from src.events_handler.on_reaction_add.on_reaction_add import OnReactionAdd
from src.events_handler.on_ready.on_ready import OnReady


class EventsHandler:

    @staticmethod
    async def handle_on_message(client: discord.Client, message: discord.Message):
        await OnMessage.handle(client, message)

    @staticmethod
    async def handle_on_ready(client: discord.Client):
        await OnReady.handle(client)

    @staticmethod
    async def handle_on_member_join(client: discord.Client, member: discord.Member):
        await OnMemberJoin.handle(client, member)

    @staticmethod
    async def handle_on_reaction_add(client: discord.Client, payload: discord.RawReactionActionEvent):
        await OnReactionAdd.handle(client, payload)

    @staticmethod
    async def handle_on_message_edit(client: discord.Client, before: discord.Message, after: discord.Message):
        await OnMessageEdit.handle(client, before, after)

    @staticmethod
    async def handle_on_message_delete(client: discord.Client, message: discord.Message):
        await OnMessageDelete.handle(client, message)
