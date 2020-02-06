import discord
import yaml


class OnMessageDelete:

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message):
        if message.guild.id != 278653494846685186 or message.author.id == 309653542354944000:
            return

        if message.author.bot or not message.content:
            return

        with open("run/config/config.yml", 'r') as stream:
            config = yaml.safe_load(stream)

        embed = discord.Embed(color=0xff0000).set_author(
            icon_url=message.author.avatar_url,
            name=f'{message.author.name}#{message.author.discriminator} ({message.author.id})'
        ) \
            .set_thumbnail(url=message.author.avatar_url) \
            .add_field(
            name="Contenue du message supprimé:",
            value=message.content,
            inline=False
        ) \
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')

        embed.description = f"Message envoyé dans le salon {message.channel.mention}."

        await message.guild.get_channel(config['channels']['log_messages']).send(
            embed=embed
        )
