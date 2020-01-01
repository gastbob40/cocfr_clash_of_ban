import discord
import yaml

from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions import PermissionChecker


async def load_custom_commands(client: discord.Client, message: discord.Message, config):

    api_manager = APIManager(config['api']['url'], config['api']['token'])

    if not PermissionChecker.is_owner(message.author):
        return await message.channel.send(
            embed=EmbedsManager.error_embed("You don't have the necessary permissions.")
        )

    state, res = api_manager.get_data('custom-commands')

    if not state:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(res)
        )

    with open('src/_data/custom_commands.yml', 'w') as file:
        documents = yaml.dump(res, file, sort_keys=True)

    return await message.channel.send(
        embed=EmbedsManager.complete_embed(f'{len(res)} custom commands have been loaded.')
    )

