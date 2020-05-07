import discord
import yaml

from src.models.role import Role
from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager


async def banned_come_back(client: discord.Client, member: discord.Member, config):
    if member.guild.id != 278653494846685186:
        return

    api_manager = APIManager(config['api']['url'], config['api']['token'])

    state, res = api_manager.get_data(
        'temp-bans',
        user_id=str(member.id),
        is_active=True,
    )

    if not res:
        return

    with open("src/_data/roles.yml", 'r') as stream:
        roles = yaml.safe_load(stream)

    role = [Role(data=x) for x in roles if x['slug'].startswith('ban')]

    for r in role:
        await member.add_roles(member.guild.get_role(r.role_id),
                               reason=f"Bantemp")

    for channel in [config['channels']['moderator'], config['channels']['log_reactions']]:
        await client.get_channel(channel).send(
            embed=EmbedsManager.sanction_embed(
                f"{member.display_name} vient de contourner son bantemp",
                f"Il avait été bantemp pour : `{res[0]['reason']}`.")
                .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
        )

    await client.get_channel( config['channels']['flood']).send(
        embed=EmbedsManager.secret_embed(
            f"je vous prie d'accueillir {member.display_name} qui vient d'essayer de contourner son ban temp.")
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
    )

    await member.send(
        embed=EmbedsManager.sanction_embed(
            f"Bonjour {member.display_name} !",
            f"Vous nous avez fait peur en quittant {member.guild.name}, mais heureusement que vous êtes revenu.\n\n"
            f"Mais ne vous inquiétez pas, nous vous avons gardé votre bantemp rien que pour vous :wink:.")
            .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
    )

    for channel in member.guild.channels:
        try:
            if isinstance(channel, discord.TextChannel):
                if member.permissions_in(channel).read_messages:
                    await channel.set_permissions(member,
                                                  send_messages=False)
            elif isinstance(channel, discord.VoiceChannel):
                if member.permissions_in(channel).connect:
                    await channel.set_permissions(member,
                                                  connect=False)
        except:
            pass
