import datetime

import discord

from src.models.post_resctriction import PostRestriction
from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions import PermissionChecker


async def verify_post(client: discord.Client, message: discord.Message, config):
    api_manager = APIManager(config['api']['url'], config['api']['token'])

    if PermissionChecker.is_moderator(message.author):
        return

    state, res = api_manager.get_data(
        'post-restrictions',
        user_id=str(message.author.id),
        channel_id=str(message.channel.id)
    )

    if not state:
        return

    now = datetime.datetime.now()
    restrictions = [PostRestriction(data=x) for x in res]

    # This is him first message => ok
    # He can post (After end time)
    if not restrictions or restrictions[0].end_time < now or now < restrictions[0].start_time:
        if not restrictions or now > restrictions[0].start_time:
            if not restrictions:
                restriction = PostRestriction()
                restriction.user_id = message.author.id
                restriction.channel_id = message.channel.id
                restriction.start_time = now + datetime.timedelta(minutes=2)
                restriction.end_time = now + datetime.timedelta(hours=config['time_between_restricted_post'])
                restriction.save()

            else:
                restrictions[0].start_time = now + datetime.timedelta(minutes=2)
                restrictions[0].end_time = now + datetime.timedelta(hours=config['time_between_restricted_post'])
                restrictions[0].update()

    else:
        # Message is not authorize
        await message.delete()
        next_post = restrictions[0].end_time

        await client.get_channel(config['channels']['log_reactions']).send(
            embed=EmbedsManager.sanction_embed(
                f"Message de {message.author.name}#{message.author.discriminator} refusé pour cause de restriction.",
                "Le joueur à été averti en message privé et le message a été supprimé."
            )
                .add_field(name='Salon', value=message.channel.mention, inline=True)
                .add_field(name='Prochain post', value=f"le {next_post.day}/{next_post.month}/{next_post.year}"
                                                       f" à {next_post.hour}:{next_post.minute}.", inline=True)
                .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
        )

        await message.author.send(
            embed=EmbedsManager.sanction_embed(
                f"Votre message a été refusé pour cause de restriction.",
                "Pour des raisons d'équités entre les joueurs, vous ne pouvez envoyer de message sur ce salon"
                " qu'une fois toutes les 22 heures."
            )
                .add_field(name='Salon', value=message.channel.mention, inline=True)
                .add_field(name='Prochain post', value=f"Le {next_post.day}/{next_post.month}/{next_post.year}"
                                                       f" à {next_post.hour}:{next_post.minute}.", inline=True)
                .set_footer(icon_url=client.user.avatar_url, text='Made By Gastbob40')
        )
