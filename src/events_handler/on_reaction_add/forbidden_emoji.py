import discord

from src.utils.embeds_manager import EmbedsManager


async def forbidden_emoji(client: discord.Client, payload: discord.RawReactionActionEvent, config):
    user = client.get_guild(payload.guild_id).get_member(payload.user_id)
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    await client.get_channel(config['channels']['moderator']).send(
        embed=EmbedsManager.sanction_embed(
            f"{user.name}#{user.discriminator} vient d'utiliser un émoji interdit.",
            "Le joueur à été averti en message privé et la réaction a été supprimé."
        )
            .add_field(name='Emoji', value=payload.emoji, inline=True)
            .add_field(name='Salon', value=channel.mention, inline=True)
            .add_field(name="Lien", value=f"[{message.jump_url}]({message.jump_url})", inline=False)
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
    )

    await client.get_channel(config['channels']['log_reactions']).send(
        embed=EmbedsManager.sanction_embed(
            f"{user.name}#{user.discriminator} vient d'utiliser un émoji interdit.",
            "Le joueur à été averti en message privé et la réaction a été supprimé."
        )
            .add_field(name='Emoji', value=payload.emoji, inline=True)
            .add_field(name='Salon', value=channel.mention, inline=True)
            .add_field(name="Lien", value=f"[{message.jump_url}]({message.jump_url})", inline=False)
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
    )

    await user.send(
        embed=EmbedsManager.sanction_embed(
            f"Vous venez d'utiliser un émoji interdit.",
            "Cet incident a été remonté aux modérateurs.\n\n"
            "Sachez que vous risquez jusqu'à un bannissement définitif en utilisant des réactions inappropriées.\n\n"
            f"Merci de lire les {client.get_channel(280735672527224842).mention}."
        )
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
    )

    await message.remove_reaction(payload.emoji, user)
