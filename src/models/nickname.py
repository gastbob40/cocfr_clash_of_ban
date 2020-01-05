import datetime

import yaml

from src.utils.api_manager import APIManager

with open("run/config/config.yml", 'r') as stream:
    data = yaml.safe_load(stream)
    api_manager = APIManager(
        data['api']['url'],
        data['api']['token']
    )


class Nickname:
    id: int
    user_id: int
    nickname: str
    time: datetime.date

    def __init__(self, **kwargs):
        """
        Init of the class
        :param kwargs: a warn from the api
        """
        if 'data' in kwargs:
            self.id = int(kwargs['data']['id'])
            self.user_id = int(kwargs['data']['user_id'])
            self.nickname = kwargs['data']['nickname']
            self.time = datetime.datetime.strptime(kwargs['data']['time'], '%Y-%m-%dT%H:%M:%S')
        else:
            self.id = -1
            self.user_id = -1
            self.nickname = "nickname"
            self.time = datetime.datetime.now()

    def save(self):
        state, r = api_manager.post_data('nicknames',
                                         user_id=str(self.user_id),
                                         nickname=self.nickname,
                                         time=self.time.strftime('%Y-%m-%dT%H:%M:%S'))

        if state:
            self.id = r['id']

    def update(self):
        state, r = api_manager.edit_data('nicknames',
                                         self.id,
                                         user_id=str(self.user_id),
                                         nickname=self.nickname,
                                         time=self.time.strftime('%Y-%m-%dT%H:%M:%S'))

    def delete(self):
        state, r = api_manager.delete_data('nicknames',
                                           self.id)

    def __str__(self):
        return f'{self.user_id} - {self.nickname} - {self.time.strftime("%Y-%m-%dT%H:%M:%SZ")}'
