from typing import List

import discord


async def commands_list(client: discord.Client, message: discord.Message, args: List[str], config):
    await message.channel.send(
        embed=discord.Embed(color=0xFFFFFF)
            .set_author(
            icon_url='https://cdn.mee6.xyz/assets/logo.png',
            name='Liste des commandes de MEE6'
        )
            .set_thumbnail(url='https://cdn.mee6.xyz/assets/logo.png')
            .add_field(
            name="!rank",
            value='Permet de voir votre niveau.',
            inline=False
        )
            .add_field(
            name="!level",
            value="Permet de voir tout les grades du serveur ainsi que le nombre d'xp gagnés par message"
                  " et par minute.",
            inline=False
        )
            .add_field(
            name="!levels",
            value="Permet de voir votre rang dans le serveur par rapport aux autres ainsi que de changer l'apparence de"
                  " la carte du rank.",
            inline=False
        )
    )

    await message.channel.send(
        embed=discord.Embed(color=0xFFFFFF)
            .set_author(
            icon_url='https://images.emojiterra.com/google/android-10/512px/1f382.png',
            name='Liste de diverses commandes'
        )
            .set_thumbnail(url='https://images.emojiterra.com/google/android-10/512px/1f382.png')
            .add_field(
            name="!change_nick <pseudo>",
            value='Permet de changer de pseudo 1 fois par semaine',
            inline=False
        )
            .add_field(
            name="!anniv add <jj> <mm>",
            value="Permet d'ajouter votre date anniversaire",
            inline=False
        )
    )

    await message.channel.send(
        embed=discord.Embed(color=0xFFFFFF)
            .set_author(
            icon_url='https://img.utdstc.com/icons/clash-of-clans-android.png:l',
            name='Liste de commandes Clash of Clans'
        )
            .set_thumbnail(url='https://img.utdstc.com/icons/clash-of-clans-android.png:l')
            .add_field(
            name="!hdv8",
            value="Permet d'afficher une playlist des compos HDV 8",
            inline=False
        )
            .add_field(
            name="!hdv9",
            value="Permet d'afficher une playlist des compos HDV 9",
            inline=False
        )
            .add_field(
            name="!hdv10",
            value="Permet d'afficher une playlist des compos HDV 10",
            inline=False
        )
            .add_field(
            name="!hdv11",
            value="Permet d'afficher une playlist des compos HDV 11",
            inline=False
        )
            .add_field(
            name="!hdv12",
            value="Permet d'afficher une playlist des compos HDV 12",
            inline=False
        )
            .add_field(
            name="!hdv13",
            value="Permet d'afficher une playlist des compos HDV 13",
            inline=False
        )
            .add_field(
            name="!village",
            value="Permet d'afficher une playlist de plan des villages GDC, Farm et Rush à partir de l'HDV 8",
            inline=False
        )
    )

    await message.channel.send(
        embed=discord.Embed(color=0xFFFFFF)
            .set_author(
            icon_url='https://images.emojiterra.com/google/android-10/512px/1f3b6.png',
            name='Liste des commandes de musique'
        )
            .set_thumbnail(url='https://images.emojiterra.com/google/android-10/512px/1f3b6.png')
            .add_field(
            name="/join",
            value="Permet de faire venir le bot",
            inline=False
        )
            .add_field(
            name="/leave",
            value="Permet de faire quitter le bot",
            inline=False
        )
            .add_field(
            name="/play <nom ou lien Youtube>",
            value="Permet d'ajouter la musique",
            inline=False
        )
            .add_field(
            name="/skip",
            value="Permet de faire passer la musique",
            inline=False
        )
            .add_field(
            name="/q",
            value="Permet d'afficher la playlist des musiques",
            inline=False
        )
            .add_field(
            name="/np",
            value="Permet de savoir où en est la playlist",
            inline=False
        )
            .add_field(
            name="/rm <numero dans la liste>",
            value="Permet de supprimer sa musique",
            inline=False
        )
    )

    await message.channel.send(
        embed=discord.Embed(color=0xFFFFFF)
            .set_author(
            icon_url='https://i.pinimg.com/originals/90/fa/0b/90fa0bddac5ce0d9b0d9a4569195bbdd.png',
            name='Liste des commandes de karaoke'
        )
            .set_thumbnail(url='https://i.pinimg.com/originals/90/fa/0b/90fa0bddac5ce0d9b0d9a4569195bbdd.png')
            .add_field(
            name="!play",
            value="Permet l'utilisation du bot en karaoké",
            inline=False
        )
            .add_field(
            name="!add",
            value="Permet d'ajouter la musique",
            inline=False
        )
            .add_field(
            name="!vote-skip",
            value="Permet de faire passer la musique",
            inline=False
        )
            .add_field(
            name="!leave",
            value="Permet de faire quitter le bot",
            inline=False
        )
    )
