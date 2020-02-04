import discord
import yaml


class OnMessageEdit:

    @staticmethod
    async def handle(client: discord.Client, before: discord.Message, after: discord.Message):
        if before.guild.id != 278653494846685186 or after.author.id == 309653542354944000:
            return

        if after.author.bot or not before.content or not after.content:
            return

        with open("run/config/config.yml", 'r') as stream:
            config = yaml.safe_load(stream)

        embed = discord.Embed(color=0xffa500).set_author(
            icon_url=before.author.avatar_url,
            name=f'{before.author.name}#{before.author.discriminator} ({before.author.id})'
        ) \
            .set_thumbnail(url=before.author.avatar_url) \
            .add_field(
            name="Contenue de l'ancien message :",
            value=after.content,
            inline=False
        ) \
            .add_field(
            name="Contenue du nouveau message :",
            value=after.content,
            inline=False
        ) \
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')

        await after.guild.get_channel(config['channels']['log_messages']).send(
            embed=embed
        )
