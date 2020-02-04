from typing import List

import discord

from src.utils.embeds_manager import EmbedsManager


async def donation_ask(client: discord.Client, message: discord.Message, args: List[str], config):
    # Display help
    if args and args[0] == '-h':
        return await message.channel.send(
            embed=EmbedsManager.information_embed("**Rappel de la commande de don :**\n\n"
                                                  "`!don`.")
        )

    donation_link = 'http://clash-of-clans-francais.ovh/faire-un-don/'

    await message.author.send(
        embed=discord.Embed(color=0xFFFFFF)
            .set_author(
            icon_url='https://pbs.twimg.com/profile_images/1142194267319873541/imd-tTed_400x400.jpg',
            name='Commande de don'
        )
            .set_thumbnail(url='https://pbs.twimg.com/profile_images/1142194267319873541/imd-tTed_400x400.jpg')
            .add_field(
            name="Vous pouvez suivre les instructions suivantes pour effectuer un don.",
            value=f'Le site de don est le suivant : [{donation_link}]({donation_link})\n\n'
                  f'Votre identifiant unique est `{message.author.id}`',
            inline=False
        )
    )

    await message.channel.send(
        embed=EmbedsManager.complete_embed(
            'Les informations concernants les dons vous ont été envoyé en message privé.')
    )
