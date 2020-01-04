import discord

from src.utils.embeds_manager import EmbedsManager


async def mention_moderator(client: discord.Client, message: discord.Message, config):
    role: discord.Role

    for role in message.role_mentions:
        if role.id == 490155585371766814:
            archer_role: discord.Role = message.guild.get_role(497451928058462221)

            if not archer_role in message.author.roles:
                return await message.channel.send(
                    embed=EmbedsManager.error_embed(
                        f"Erreur, il faut être niveau 5 (soit {archer_role.name}) afin de mentionner un modérateur.\n"
                        f"Vous pouvez cependant vous adresser à un modérateur connecté."
                    )
                        .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
                )

            await client.get_channel(config['channels']['moderator']).send(
                embed=EmbedsManager.sanction_embed(
                    f"{message.author.name}#{message.author.discriminator} vient de mentionner les modérateurs."
                )
                    .add_field(name='Message', value=message.content, inline=True)
                    .add_field(name='Salon', value=message.channel.mention, inline=True)
                    .add_field(name="Lien", value=f"[{message.jump_url}]({message.jump_url})", inline=False)
                    .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
            )

            await client.get_channel(config['channels']['log_reactions']).send(
                embed=EmbedsManager.sanction_embed(
                    f"{message.author.name}#{message.author.discriminator} vient de mentionner les modérateurs."
                )
                    .add_field(name='Message', value=message.content, inline=True)
                    .add_field(name='Salon', value=message.channel.mention, inline=True)
                    .add_field(name="Lien", value=f"[{message.jump_url}]({message.jump_url})", inline=False)
                    .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
            )

            mentionable_message = ''
            for modo in message.guild.get_role(278656056228315136).members:
                mentionable_message += modo.mention

            msg: discord.Message = await message.channel.send(mentionable_message)
            await msg.delete()

