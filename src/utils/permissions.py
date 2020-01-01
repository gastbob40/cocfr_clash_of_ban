import os

import discord
import yaml

from src.models.role import Role


class PermissionChecker:

    @staticmethod
    def is_owner(member: discord.Member):
        with open("run/config/config.yml", 'r') as stream:
            data = yaml.safe_load(stream)

        return member.id == data['owner_id']

    @staticmethod
    def is_moderator(member: discord.Member):

        with open("run/config/config.yml", 'r') as stream:
            data = yaml.safe_load(stream)

        if member.id == data['owner_id']:
            return True

        if not os.path.exists('src/_data/roles.yml'):
            return False

        with open("src/_data/roles.yml", 'r') as stream:
            roles = yaml.safe_load(stream)

        moderator_role = [Role(data=x) for x in roles if x['slug'] == 'moderator']

        return len(moderator_role) != 0 and member.guild.get_role(moderator_role[0].role_id) in member.roles
