import discord
import yaml

from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions import PermissionChecker


async def load_roles(client: discord.Client, message: discord.Message, config):

    api_manager = APIManager(config['api']['url'], config['api']['token'])

    if not PermissionChecker.is_owner(message.author):
        return await message.channel.send(
            embed=EmbedsManager.error_embed("You don't have the necessary permissions.")
        )

    state, res = api_manager.get_data('roles')

    if not state:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(res)
        )

    with open('src/_data/roles.yml', 'w') as file:
        documents = yaml.dump(res, file, sort_keys=True)

    return await message.channel.send(
        embed=EmbedsManager.complete_embed(f'{len(res)} roles have been loaded.')
    )

