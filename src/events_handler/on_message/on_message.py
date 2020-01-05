from typing import List

import discord
import yaml

from src.events_handler.on_message.miscs.change_nick import change_nick
from src.events_handler.on_message.miscs.commands_list import commands_list
from src.events_handler.on_message.miscs.mention_moderator import mention_moderator
from src.events_handler.on_message.moderation.bantemp_member import bantemp_member
from src.events_handler.on_message.moderation.unbantemp_member import unbantemp_member
from src.events_handler.on_message.post_restriction.verify_post import verify_post
from src.events_handler.on_message.moderation.warn_member import warn_member
from src.events_handler.on_message.post_restriction.reinit_restriction import reinit_restriction
from src.events_handler.on_message.setup.load_custom_commands import load_custom_commands
from src.events_handler.on_message.setup.load_roles import load_roles
from src.events_handler.on_message.update.update import Update
from src.models.custom_command import CustomCommand


class OnMessage:

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message):

        if message.guild == None or message.author.bot:
            return

        with open("run/config/config.yml", 'r') as stream:
            config = yaml.safe_load(stream)

        prefix = config['bot']['prefix']

        if message.role_mentions:
            await mention_moderator(client, message, config)

        if message.channel.id in config['restricted_channels']:
            await verify_post(client, message, config)

        await Update.handle(client, message, config)

        if not message.content or not message.content.startswith(prefix):
            return

        command = message.content.split(' ')[0][1:]
        args = message.content.split(' ')[1:]

        # Owner command
        if command == 'load_roles':
            await load_roles(client, message, args, config)
        elif command == 'load_commands':
            await load_custom_commands(client, message, args, config)

        # Moderator command
        elif command in ['av', 'avertissement']:
            await warn_member(client, message, args, config)
        elif command in ['bt', 'bantemp']:
            await bantemp_member(client, message, args, config)
        elif command in ['eb', 'enleverban']:
            await unbantemp_member(client, message, args, config)
        elif command in ['r', 'reinit']:
            await reinit_restriction(client, message, args, config)

        # Public command
        elif command in ['co', 'commandes']:
            await commands_list(client, message, args, config)
        elif command in ['cn', 'change_nick']:
            await change_nick(client, message, args, config)

        else:
            with open("src/_data/custom_commands.yml", 'r') as stream:
                custom_commands = [CustomCommand(data=x) for x in yaml.safe_load(stream)]

            custom_command: List[CustomCommand] = [x for x in custom_commands if x.trigger == command]

            if custom_command and custom_command[0].is_active:
                await message.channel.send(
                    custom_command[0].message
                )
