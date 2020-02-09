from datetime import timedelta
from typing import List

import discord
import yaml
import math

from src.models.role import Role
from src.models.temp_ban import TempBan
from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions import PermissionChecker


async def bantemp_member(client: discord.Client, message: discord.Message, args: List[str], config):
    api_manager = APIManager(config['api']['url'], config['api']['token'])

    if not PermissionChecker.is_moderator(message.author):
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Vous n'avez pas les permissions nécessaires.")
        )

    # Display help
    if args and args[0] == '-h':
        return await message.channel.send(
            embed=EmbedsManager.information_embed("**Rappel de la commande de bannissement temporaire :**\n\n"
                                                  "`!bt <@user> <durée> <reason>`.")
        )

    # Check if target exist
    target: discord.Member = message.mentions[0] if len(message.mentions) == 1 else False

    if not target:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Erreur dans la commande. Vous devez mentionner un utilisateur.")
        )

    args = args[1:]

    if len(args) == 0:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Erreur dans la commande. Vous devez spécifié une durée.")
        )

    bantemp = TempBan()
    bantemp.user_id = target.id
    bantemp.moderator_id = message.author.id

    if args[0].isdigit():
        if int(args[0]) < 24:
            delta = f'{int(args[0])} heure(s)'
        elif int(args[0]) % 24 == 0:
            delta = f'{int(args[0]) / 24} jour(s)'
        else:
            delta = f'{math.floor(int(args[0]) / 24)} jour(s) et {int(args[0]) % 24} heure(s)'

        bantemp.end_time += timedelta(hours=int(args[0]))

    elif args[0] and args[0][-1] == 'd' and args[0][:-1].isdigit():
        delta = f'{int(args[0][:-1])} jour(s)'
        bantemp.end_time += timedelta(days=int(args[0][:-1]))

    else:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(f"Erreur dans la commande. La date spécifiée est incorrecte (`{args[0]}`).")
        )

    args = args[1:]

    if len(args) == 0:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Erreur dans la commande. Vous devez spécifié une raison.")
        )

    bantemp.reason = ' '.join(args)

    bantemp.save()

    await message.channel.send(
        embed=EmbedsManager.sanction_embed(
            f"Bannissement temporaire du membre {target.display_name} pour une durée de {delta}.",
            f"Ce joueur ne respecte toujours pas les règles malgré un rappel d'un Modérateur, il prend donc un BanTemp")
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
            .add_field(name="Rappel :",
                       value="Sachez que plusieurs BanTemp peuvent conduire à un Bannissement définitif du serveur!\n\n"
                             f"Pour évitez cela, prenez connaissance des {client.get_channel(280735672527224842).mention} qui ne"
                             f" sont pas nombreuses mais importantes pour le bon fonctionnement du serveur.",
                       inline=False)
            .add_field(name="Raison :", value=bantemp.reason, inline=True)
            .add_field(name="Durée :", value=delta, inline=True)
            .set_image(
            url='https://cdn.discordapp.com/attachments/377179445640822784/663478346763599872/photostudio_15295854416791.png'
        )
    )

    await client.get_channel(config['channels']['log_reactions']).send(
        embed=EmbedsManager.sanction_embed(
            f"Bannissement temporaire du membre {target.display_name} pour une durée de {delta}.",
            f"Il a été bantemp pour : `{bantemp.reason}`.")
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
            .add_field(name="Durée :", value=delta, inline=True)
            .add_field(name="Auteur :", value=message.author.display_name, inline=True)
    )

    await target.send(
        embed=EmbedsManager.sanction_embed(
            f"Vous venez de subir un bannissement temporaire de {delta}.",
            f"Vous venez d'être bantemp pour : `{bantemp.reason}`.\n\n"
            f"Sachez que plusieurs bans temporaires conduisent à un ban définitif.")
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')

            .add_field(name="Durée :", value=delta, inline=True)
            .add_field(name="Auteur :", value=message.author.display_name, inline=True)
    )

    # Add roles

    with open("src/_data/roles.yml", 'r') as stream:
        roles = yaml.safe_load(stream)

    role = [Role(data=x) for x in roles if x['slug'].startswith('ban')]

    for r in role:
        await target.add_roles(message.guild.get_role(r.role_id),
                               reason=f"Bantemp pour {bantemp.reason} pour une durée de {delta}")

    for channel in message.guild.channels:
        try:
            if target.permissions_in(channel).read_messages:
                await channel.set_permissions(target,
                                              send_messages=False)
            if target.permissions_in(channel).connect:
                await channel.set_permissions(target,
                                              connect=False)
        except:
            pass
