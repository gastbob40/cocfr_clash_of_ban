from typing import List

import discord

from src.models.warn import Warn
from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions import PermissionChecker


async def warn_member(client: discord.Client, message: discord.Message, args: List[str], config):
    api_manager = APIManager(config['api']['url'], config['api']['token'])

    if not PermissionChecker.is_moderator(message.author):
        return await message.channel.send(
            embed=EmbedsManager.error_embed("You don't have the necessary permissions.")
        )

    # Display help
    if args and args[0] == '-h':
        return await message.channel.send(
            embed=EmbedsManager.information_embed("**Warning command reminder:**\n\n"
                                                  "`!av <@user> <reason>`.")
        )

    # Check if target exist
    target: discord.Member = message.mentions[0] if len(message.mentions) == 1 else False

    if not target:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Error in the command. You must mention an user.")
        )

    args = args[1:]

    if len(args) == 0:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Error in the command. You must add a reason.")
        )

    warn = Warn()
    warn.user_id = target.id
    warn.moderator_id = message.author.id
    warn.reason = ' '.join(args)

    warn.save()

    await message.channel.send(
        embed=EmbedsManager.sanction_embed(
            f"Avertissement du membre {target.display_name}.",
            f"Vous venez de l'avertir pour : `{warn.reason}`.")
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
    )

    await client.get_channel(config['channels']['log_reactions']).send(
        embed=EmbedsManager.sanction_embed(
            f"Avertissement du membre {target.display_name}.",
            f"Il a été averti pour : `{warn.reason}`.")
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
            .add_field(name="Auteur :", value=message.author.display_name)
    )

    await target.send(
        embed=EmbedsManager.sanction_embed(
            f"Vous venez de subir un avertissement.",
            f"Vous venez d'être averti pour : `{warn.reason}`.")
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
            .add_field(name="Auteur :", value=message.author.display_name)
    )
