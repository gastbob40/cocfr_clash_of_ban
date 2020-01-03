from typing import List

import discord
import yaml

from src.models.role import Role
from src.models.temp_ban import TempBan
from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions import PermissionChecker


async def unbantemp_member(client: discord.Client, message: discord.Message, args: List[str], config):
    api_manager = APIManager(config['api']['url'], config['api']['token'])

    if not PermissionChecker.is_moderator(message.author):
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Vous n'avez pas les permissions nécessaires.")
        )

    # Display help
    if args and args[0] == '-h':
        return await message.channel.send(
            embed=EmbedsManager.information_embed("**Rappel de la commande de bannissement temporaire :**\n\n"
                                                  "`!eb <@user>`.")
        )

    # Check if target exist
    target: discord.Member = message.mentions[0] if len(message.mentions) == 1 else False

    if not target:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Erreur dans la commande. Vous devez mentionner un utilisateur.")
        )

    state, res = api_manager.get_data(
        'temp-bans',
        user_id=str(target.id),
        is_active=True,
    )

    if not state:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Erreur dans l'api. Merci de contacter gast.")
        )

    if len(res) == 0:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(f"Erreur dans la commande. {target.display_name} n'a pas de bantemp actif")
        )

    # Remove roles

    with open("src/_data/roles.yml", 'r') as stream:
        roles = yaml.safe_load(stream)

    role = [Role(data=x) for x in roles if x['slug'].startswith('ban')]

    for r in role:
        await target.remove_roles(message.guild.get_role(r.role_id))

    # Send message

    await message.channel.send(
        embed=EmbedsManager.sanction_embed(
            f"Vous venez de retirer le bantemp de {target.display_name}"
        )
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
    )

    await client.get_channel(config['channels']['log_reactions']).send(
        embed=EmbedsManager.sanction_embed(
            f"Le bantemp de {target.display_name} vient d'être retiré.",
            f"Auteur : {message.author.display_name}")
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
    )

    await target.send(
        embed=EmbedsManager.sanction_embed(
            "Un modérateur vient de retirer votre bantemp."
        )
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
    )

    # Update data

    temp_bans = [TempBan(data=x) for x in res]

    for bt in temp_bans:
        bt.is_active = False
        bt.update()

    # Reset permission

    for channel in message.guild.channels:
        try:
            if not target.permissions_in(channel).send_messages or not target.permissions_in(channel).connect:
                await channel.set_permissions(target,
                                              overwrite=None)
        except:
            pass
