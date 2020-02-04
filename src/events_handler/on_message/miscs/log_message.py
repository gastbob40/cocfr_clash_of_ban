import discord


async def log_message(client: discord.Client, message: discord.Message, config):
    if message.author.id == config['owner_id']:
        return

    embed = discord.Embed(color=0x00FF00).set_author(
        icon_url=message.author.avatar_url,
        name=f'{message.author.name}#{message.author.discriminator} ({message.author.id})'
    ) \
        .set_thumbnail(url=message.author.avatar_url)

    if message.content:
        embed.add_field(
            name="Contenue du nouveau message:",
            value=message.content
        )

    if message.attachments:
        embed.set_image(url=message.attachments[0].url)

    try:
        await message.guild.get_channel(config['channels']['log_messages']).send(
            embed=embed
        )
    except:
        pass
