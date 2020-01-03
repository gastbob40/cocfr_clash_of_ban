import datetime
import discord
import yaml

from src.events_handler.on_message.update.update_bantemp import update_bantemp
from src.models.role import Role
from src.models.temp_ban import TempBan
from src.utils.api_manager import APIManager


class Update:

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message, config):
        last_update = datetime.datetime.strptime(config['update']['last_update'], '%Y-%m-%dT%H:%M:%SZ')
        now = datetime.datetime.now()

        if last_update + datetime.timedelta(minutes=int(config['update']['time_between_update'])) > now:
            return

        config['update']['last_update'] = now.strftime('%Y-%m-%dT%H:%M:%SZ')

        with open('run/config/config.yml', 'w') as file:
            documents = yaml.dump(config, file, sort_keys=True)

        api_manager = APIManager(config['api']['url'], config['api']['token'])

        state, res = api_manager.get_data('updates')

        if not state:
            return

        with open("src/_data/roles.yml", 'r') as stream:
            roles = yaml.safe_load(stream)

        role = [Role(data=x) for x in roles if x['slug'].startswith('ban')]

        for bt in res['TempBan']:
            await update_bantemp(client, message, TempBan(data=bt), role, config)
