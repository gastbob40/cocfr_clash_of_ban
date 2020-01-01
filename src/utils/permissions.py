import discord
import yaml


class PermissionChecker:

    @staticmethod
    def is_owner(member: discord.Member):
        with open("run/config/config.yml", 'r') as stream:
            data = yaml.safe_load(stream)

        return member.id == data['owner_id']