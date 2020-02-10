import discord
import yaml

from src.events_handler.events_handler import EventsHandler

client = discord.Client()
with open("run/config/config.yml", 'r') as stream:
    data = yaml.safe_load(stream)


@client.event
async def on_ready():
    await EventsHandler.handle_on_ready(client)


@client.event
async def on_message(message):
    await EventsHandler.handle_on_message(client, message)


@client.event
async def on_member_join(member):
    await EventsHandler.handle_on_member_join(client, member)


@client.event
async def on_raw_reaction_add(payload):
    await EventsHandler.handle_on_reaction_add(client, payload)


@client.event
async def on_message_edit(before, after):
    await EventsHandler.handle_on_message_edit(client, before, after)


@client.event
async def on_message_delete(message):
    await EventsHandler.handle_on_message_delete(client, message)

client.run(data['bot']['token'])
