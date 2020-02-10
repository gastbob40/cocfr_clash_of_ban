import discord
import yaml

from src.events_handler.on_reaction_add.forbidden_emoji import forbidden_emoji


class OnReady:

    @staticmethod
    async def handle(client: discord.Client):
        print('We have logged in as {0.user}'.format(client))

        invites = await client.get_guild(278653494846685186).invites()
        data = [{
            'uses': invite.uses,
            'author': invite.inviter.id,
            'url': invite.url
        } for invite in invites]

        with open('src/_data/invites.yml', 'w') as file:
            yaml.dump(data, file)
