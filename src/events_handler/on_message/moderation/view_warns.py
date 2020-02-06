from typing import List

import discord

from src.models.warn import Warn
from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions import PermissionChecker


async def view_warns(client: discord.Client, message: discord.Message, args: List[str], config):
    api_manager = APIManager(config['api']['url'], config['api']['token'])

    if not PermissionChecker.is_moderator(message.author) and len(message.mentions):
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Vous n'avez pas les permissions nécessaires.")
        )

    channel = 289476916044627978
    if not PermissionChecker.is_moderator(message.author) and message.channel.id != channel:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Hum, vous n'êtes pas dans le bon salon.\n\n"
                                            f"Merci de réessayer dans {message.guild.get_channel(channel).mention}.")
        )

    # Display help
    if args and args[0] == '-h':
        return await message.channel.send(
            embed=EmbedsManager.information_embed("**Rappel de la commande de visualisation des avertissements :**\n\n"
                                                  "`!ia <?@user>`.")
        )

    # Check if target exist
    target: discord.Member = message.mentions[0] if len(message.mentions) == 1 else message.author

    state, res = api_manager.get_data('warns', user_id=target.id)

    if not state:
        return

    if not res:
        return await message.channel.send(
            embed=EmbedsManager.sanction_embed(
                f"Le membre {target.name}#{target.discriminator} n'a aucun avertissement:",
            )
                .set_thumbnail(url=target.avatar_url)
                .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
        )

    if len(res) > 20:
        return await message.channel.send(
            EmbedsManager.error_embed(
                f"Hum, on dirait que {target.name}#{target.discriminator} a trop d'avertissements :(\n"
                f"Je vous conseille d'aller sur le site web afin de pouvoir voir la liste detaillée."
            )
        )

    warns = [Warn(data=x) for x in res]
    embed = EmbedsManager.sanction_embed(
        f"Voici les informations concernants {target.name}#{target.discriminator} :"
    ) \
        .set_thumbnail(url=target.avatar_url) \
        .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')

    for warn in warns:
        moderator = message.guild.get_member(warn.moderator_id) if \
            message.guild.get_member(warn.moderator_id) else \
            'Un ancien modérateur'

        embed.add_field(
            name=f"Avertissement de {moderator}, le {warn.time.strftime('%d/%m/%Y à %H:%M')}",
            value=f"Avertissement pour `{warn.reason}`",
            inline=False
        )

    await message.channel.send(embed=embed)
