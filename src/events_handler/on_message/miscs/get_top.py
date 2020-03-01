import math
from datetime import timedelta
from typing import List

import discord
import yaml

from src.models.role import Role
from src.models.temp_ban import TempBan
from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions import PermissionChecker


async def get_top(client: discord.Client, message: discord.Message, args: List[str], config):
    api_manager = APIManager(config['api']['url'], config['api']['token'])

    if not PermissionChecker.is_moderator(message.author):
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Vous n'avez pas les permissions nécessaires.")
        )

    # Display help
    if args and args[0] == '-h':
        return await message.channel.send(
            embed=EmbedsManager.information_embed(
                "**Rappel de la commande de récupération des meilleurs messages :**\n\n"
                "`!top`.")
        )

    # Get channel and messages
    channel: discord.TextChannel = message.guild.get_channel(config['channels']['top'])

    john_message: discord.Message = await channel.fetch_message(id=683660205250183198)

    messages: List[discord.Message] = await channel.history(limit=None, after=john_message.edited_at).flatten()

    # Get cleaned data
    emoji = '👍'
    records = []
    for msg in messages:
        if not msg.author.bot:
            for reaction in msg.reactions:
                if reaction.emoji == emoji:
                    records.append({
                        'author': msg.author,
                        'content': msg.content,
                        'date': msg.created_at,
                        'link': msg.jump_url,
                        'count': reaction.count
                    })

    # Sort data
    records = sorted(records, key=lambda x: x['count'], reverse=True)

    # Get just the 10 best records
    records = records[:10]

    for index, record in enumerate(records):
        embed = discord.Embed(color=0xff0000) \
            .set_author(
            name=f"Message {index + 1}."
        ) \
            .add_field(
            name="Contenu du message",
            value=record['content'],
            inline=False
        ) \
            .add_field(
            name="Nombre de vote (👍) :",
            value=record['count'],
            inline=True
        ) \
            .add_field(
            name="Lien du message",
            value=record['link'],
            inline=True
        ) \
            .set_thumbnail(url=record['author'].avatar_url)

        embed.description = f"Proposition de {record['author'].name}#{record['author'].discriminator} " \
                            f"({record['author'].id})"

        await message.channel.send(
            embed=embed
        )
