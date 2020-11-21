from datetime import timedelta

import discord, math
import yaml

from src.models.role import Role
from src.models.temp_ban import TempBan
from src.utils.embeds_manager import EmbedsManager


async def forbidden_emoji(client: discord.Client, payload: discord.RawReactionActionEvent, config):
    user = await client.get_guild(payload.guild_id).fetch_member(payload.user_id)
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    time = 48
    delta = "2 jours"

    await client.get_channel(config['channels']['log_reactions']).send(
        embed=EmbedsManager.sanction_embed(
            f"{user.name}#{user.discriminator} vient d'utiliser un émoji interdit.",
            f"Le joueur à été averti en message privé, la réaction a été supprimé et il a été bantemp {time} heures."
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
            f"Vous écopez d'un bannisement temporaire de {time} heures suite à votre utilisation de "
            f"réactions inappropriées.\n\n"
            f"Merci de lire les {client.get_channel(280735672527224842).mention}."
        )
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
    )

    # Remove reaction
    await message.remove_reaction(payload.emoji, user)

    # Log bt
    bantemp = TempBan()
    bantemp.user_id = user.id
    bantemp.moderator_id = client.user.id
    bantemp.reason = "BanTemp suite à une réaction inappropriée."
    bantemp.end_time += timedelta(hours=time)
    bantemp.save()

    # Change permissions

    with open("src/_data/roles.yml", 'r') as stream:
        roles = yaml.safe_load(stream)

    role = [Role(data=x) for x in roles if x['slug'].startswith('ban')]

    for r in role:
        await user.add_roles(message.guild.get_role(r.role_id),
                               reason=f"Bantemp pour {bantemp.reason} pour une durée de {delta}")

    for channel in message.guild.channels:
        try:
            if user.permissions_in(channel).read_messages:
                await channel.set_permissions(user,
                                              send_messages=False)
            if user.permissions_in(channel).connect:
                await channel.set_permissions(user,
                                              connect=False)
        except:
            pass



