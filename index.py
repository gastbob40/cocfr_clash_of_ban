import discord
import yaml

from src.events_handler.events_handler import EventsHandler

client = discord.Client()
with open("run/config/config.yml", 'r') as stream:
    data = yaml.safe_load(stream)


@client.event
async def on_ready():
    EventsHandler.handle_on_ready(client)


@client.event
async def on_message(message):
    await EventsHandler.handle_on_message(client, message)


client.run(data['bot']['token'])
