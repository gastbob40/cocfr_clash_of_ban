from datetime import timedelta
from typing import List

import discord
import yaml

from src.models.post_resctriction import PostRestriction
from src.models.role import Role
from src.models.temp_ban import TempBan
from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions import PermissionChecker


async def reinit_restriction(client: discord.Client, message: discord.Message, args: List[str], config):
    api_manager = APIManager(config['api']['url'], config['api']['token'])

    if not PermissionChecker.is_moderator(message.author):
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Vous n'avez pas les permissions nécessaires.")
        )

    # Display help
    if args and args[0] == '-h':
        return await message.channel.send(
            embed=EmbedsManager.information_embed("**Rappel de la commande de rénitialistion de restriction :**\n\n"
                                                  "`!bt <@user> <durée> <reason>`.\n\n"
                                                  "Attention, vous devez être dans le salon restreint.")
        )

    if not message.channel.id in config['restricted_channels']:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Erreur dans la commande. Vous n'êtes pas dans un salon restreint.")
        )

    # Check if target exist
    target: discord.Member = message.mentions[0] if len(message.mentions) == 1 else False

    if not target:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Erreur dans la commande. Vous devez mentionner un utilisateur.")
        )

    state, res = api_manager.get_data(
        'post-restrictions',
        user_id=str(target.id),
        channel_id=str(message.channel.id)
    )

    if not state:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Erreur dans l'api. Merci de contacter gast.")
        )

    restriction = None if not res else PostRestriction(data=res[0])

    if not restriction:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                f"Erreur dans la commande. {target.name}#{target.discriminator} n'a pas de restriction"
                f" active dans {message.channel.mention}"
            )
        )

    else:
        restriction.delete()

        await client.get_channel(config['channels']['log_reactions']).send(
            embed=EmbedsManager.sanction_embed(
                f"{message.author.name}#{message.author.discriminator} vient de retirer une restriction de "
                f"{target.name}#{target.discriminator}.",
            )
                .add_field(name='Salon', value=message.channel.mention, inline=True)
                .add_field(name='Membre', value=target.mention, inline=True)
                .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
        )

        await message.channel.send(
            embed=EmbedsManager.sanction_embed(
                f"Vous venez de retirer une restriction de "
                f"{target.name}#{target.discriminator}.",
            )
                .add_field(name='Salon', value=message.channel.mention, inline=True)
                .add_field(name='Membre', value=target.mention, inline=True)
                .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
        )

        await target.send(
            embed=EmbedsManager.sanction_embed(
                f"{message.author.name}#{message.author.discriminator} vient de vous retirer une restriction.",
            )
                .add_field(name='Salon', value=message.channel.mention, inline=True)
                .add_field(name='Membre', value=target.mention, inline=True)
                .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
        )

