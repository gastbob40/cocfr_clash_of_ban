import discord


async def log_message(client: discord.Client, message: discord.Message, config):
    embed = discord.Embed(color=0x00FF00).set_author(
        icon_url=message.author.avatar_url,
        name=f'{message.author.name}#{message.author.discriminator} ({message.author.id})'
    )\
        .set_thumbnail(url=message.author.avatar_url) \
        .add_field(
        name="Contenue du nouveau message:",
        value=message.content
    )

    if message.attachments:
        embed.set_image(url=message.attachments[0].url)

    await message.guild.get_channel(config['channels']['log_messages']).send(
        embed=embed
    )
