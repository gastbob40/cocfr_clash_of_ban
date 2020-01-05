import datetime

import yaml

from src.utils.api_manager import APIManager

with open("run/config/config.yml", 'r') as stream:
    data = yaml.safe_load(stream)
    api_manager = APIManager(
        data['api']['url'],
        data['api']['token']
    )


class Warn:
    id: int
    user_id: int
    moderator_id: int
    time: datetime.date
    reason: str

    def __init__(self, **kwargs):
        """
        Init of the class
        :param kwargs: a warn from the api
        """
        if 'data' in kwargs:
            self.id = int(kwargs['data']['id'])
            self.user_id = int(kwargs['data']['user_id'])
            self.moderator_id = int(kwargs['data']['moderator_id'])
            self.time = datetime.datetime.strptime(kwargs['data']['time'], '%Y-%m-%dT%H:%M:%S')
            self.reason = kwargs['data']['reason']
        else:
            self.id = -1
            self.user_id = -1
            self.moderator_id = -1
            self.time = datetime.datetime.now()
            self.reason = 'empty reason'

    def save(self):
        state, r = api_manager.post_data('warns',
                                         user_id=str(self.user_id),
                                         moderator_id=str(self.moderator_id),
                                         time=self.time.strftime('%Y-%m-%dT%H:%M:%S'),
                                         reason=self.reason)
        if state:
            self.id = r['id']

    def update(self):
        state, r = api_manager.edit_data('warns',
                                         self.id,
                                         user_id=str(self.user_id),
                                         moderator_id=str(self.moderator_id),
                                         time=self.time.strftime('%Y-%m-%dT%H:%M:%S'),
                                         reason=self.reason)

    def delete(self):
        state, r = api_manager.delete_data('warns',
                                           self.id)
