from typing import List

import discord

from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions import PermissionChecker


async def user_information(client: discord.Client, message: discord.Message, args: List[str], config):
    if not PermissionChecker.is_moderator(message.author):
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Vous n'avez pas les permissions nécessaires.")
        )

    # Display help
    if args and args[0] == '-h':
        return await message.channel.send(
            embed=EmbedsManager.information_embed("**Rappel de la commande d'information utilisateur :**\n\n"
                                                  "`!ui <@user>`.")
        )

    # Check if target exist
    target: discord.Member = message.mentions[0] if len(message.mentions) == 1 else False

    if not target:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Erreur dans la commande. Vous devez mentionner un utilisateur.")
        )

    await message.channel.send(
        embed=EmbedsManager.sanction_embed(
            f"Voici les informations de {target.name}#{target.discriminator} :",
        )
            .set_thumbnail(url=target.avatar_url)
            .add_field(name='Surnom', value=target.display_name, inline=True)
            .add_field(name='Tag', value=target.discriminator, inline=True)
            .add_field(name='ID', value=target.id, inline=True)
            .add_field(name='Compte créé le', value=target.created_at.strftime('%d/%m/%Y à %H:%M:%S'), inline=True)
            .add_field(name='A rejoint le serveur le', value=target.joined_at.strftime('%d/%m/%Y à %H:%M:%S'),
                       inline=True)
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
    )
