from typing import List

import discord

from src.models.role import Role
from src.models.temp_ban import TempBan
from src.utils.embeds_manager import EmbedsManager


async def update_bantemp(client: discord.Client, message: discord.Message, bantemp: TempBan, roles: List[Role], config):
    target: discord.Member = message.guild.get_member(bantemp.user_id)
    bantemp.is_active = False

    if not target:
        bantemp.update()
        return

    # Remove Roles
    for role in roles:
        await target.remove_roles(message.guild.get_role(role.role_id))

    # Send message
    await client.get_channel(config['channels']['log_reactions']).send(
        embed=EmbedsManager.sanction_embed(
            f"Le bantemp de {target.display_name} vient de finir."
        )
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
    )

    try:
        await target.send(
            embed=EmbedsManager.sanction_embed(
                f"Votre bantemp vient de finir."
            )
                .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
        )
    except:
        pass

    bantemp.update()

    for channel in message.guild.channels:
        try:
            if isinstance(channel, discord.TextChannel):
                if not target.permissions_in(channel).send_messages:
                    await channel.set_permissions(target,
                                                  overwrite=None)
            elif isinstance(channel, discord.VoiceChannel):
                if not target.permissions_in(channel).connect:
                    await channel.set_permissions(target,
                                                  overwrite=None)
        except:
            pass
