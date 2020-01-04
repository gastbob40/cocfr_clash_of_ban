import datetime
from typing import List

import discord

from src.models.nickname import Nickname
from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager


async def change_nick(client: discord.Client, message: discord.Message, args: List[str], config):
    api_manager = APIManager(config['api']['url'], config['api']['token'])

    # Display help
    if args and args[0] == '-h':
        return await message.channel.send(
            embed=EmbedsManager.information_embed("**Rappel de la commande de changement de pseudo :**\n\n"
                                                  "`!change_nick <pseudo>`.")
        )

    if not args:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Erreur dans la commande. Vous devez spécifé un pseudo")
        )

    nickname = Nickname()
    nickname.nickname = ' '.join(args)
    nickname.user_id = message.author.id

    for letter in nickname.nickname:
        if ord(letter) > 255:
            return await message.channel.send(
                embed=EmbedsManager.error_embed("Erreur dans la commande. Seul les caractères *simples* sont autorisés"
                                                " (code ASCII entre 0 et 255).")
                    .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
            )

    state, res = api_manager.get_data(
        'nicknames',
        user_id=str(message.author.id)
    )

    if not state:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Erreur dans l'api. Merci de contacter gast.")
                .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
        )

    nicknames = [Nickname(data=x) for x in res]

    nicknames = sorted(nicknames, key=lambda x: x.time, reverse=True)
    now = datetime.datetime.now()

    # He can't change
    if nicknames and nicknames[0].time < now + datetime.timedelta(days=7):
        new_date = nicknames[0].time + datetime.timedelta(days=7)
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Vous avez changé votre pseudo il y a moins de 1 semaine.\n\n"
                                            f"Vous pourrez le changer le {new_date.day}/{new_date.month}/{new_date.year}"
                                            f" à {new_date.hour}:{new_date.minute}.")
                .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
        )

    try:

        old_nickname = message.author.display_name

        await message.author.edit(nick=nickname.nickname)

        nickname.save()

        await message.channel.send(
            embed=EmbedsManager.complete_embed(
                "Vous venez de changer de pseudo avec succès.",
                f"Vos êtes dorénavant `{nickname.nickname}`."
            )
                .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
        )

        await client.get_channel(config['channels']['log_reactions']).send(
            embed=EmbedsManager.complete_embed(
                f"{message.author.name}#{message.author.discriminator} vient de changer de pseudo."
            )
                .add_field(name='Ancien pseudo', value=old_nickname, inline=True)
                .add_field(name='Nouveau pseudo', value=nickname.nickname, inline=True)
                .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
        )

    except:
        await message.channel.send(
            embed=EmbedsManager.error_embed("Hum, je n'ai pas reussi a changer votre pseudo.")
                .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
        )
