import itertools

import discord
import yaml


async def log_invite(client: discord.Client, member: discord.Member, config):
    if member.guild.id != 278653494846685186:
        return

    with open("src/_data/invites.yml", 'r') as stream:
        old_invites = yaml.safe_load(stream)

    invites = await member.guild.invites()
    new_invites = [{
        'uses': invite.uses,
        'author': invite.inviter.id,
        'url': invite.url
    } for invite in invites]

    with open('src/_data/invites.yml', 'w') as file:
        yaml.dump(new_invites, file)

    inter_sec = [item for item in old_invites if item in new_invites]
    sym_diff = [item for item in itertools.chain(old_invites, new_invites) if item not in inter_sec]

    embed = discord.Embed(color=0x19D773) \
        .set_author(icon_url=member.avatar_url,
                    name=f"Arrivé de {member.name}#{member.discriminator} ({member.id}).") \
        .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')

    if len(sym_diff) != 0:
        inviter = member.guild.get_member(sym_diff[0]['author'])

        if inviter:
            embed.description = f"A rejoint le serveur via l'invitation `{sym_diff[0]['url']}`.\n" \
                                f"Invitation de {inviter.name}#{inviter.discriminator} ({inviter.id})."
            embed.set_thumbnail(url=inviter.avatar_url)
        else:
            embed.description = f"A rejoint le serveur via l'invitation `{sym_diff[0]['url']}." \
                                f"Invité par un ancien membre du serveur.\n"

    else:
        embed.description = f"A rejoint le serveur via l'invitation `https://discord.gg/cocfr`."
        embed.set_thumbnail(url=member.guild.icon_url)

    await client.get_channel(config['channels']['log_invites']).send(
        embed=embed
    )
