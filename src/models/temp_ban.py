import datetime
import yaml
from src.utils.api_manager import APIManager

with open("run/config/config.yml", 'r') as stream:
    data = yaml.safe_load(stream)
    api_manager = APIManager(
        data['api']['url'],
        data['api']['token']
    )


class TempBan:
    id: int
    user_id: int
    moderator_id: int
    reason: str
    start_time: datetime.date
    end_time: datetime.date
    is_active: bool

    def __init__(self, **kwargs):
        """
        Init of the class
        :param kwargs: a warn from the api
        """
        if 'data' in kwargs:
            self.id = int(kwargs['data']['id'])
            self.user_id = int(kwargs['data']['user_id'])
            self.moderator_id = int(kwargs['data']['moderator_id'])
            self.start_time = datetime.datetime.strptime(kwargs['data']['start_time'], '%Y-%m-%dT%H:%M:%S')
            self.end_time = datetime.datetime.strptime(kwargs['data']['end_time'], '%Y-%m-%dT%H:%M:%S')
            self.reason = kwargs['data']['reason']
            self.is_active = kwargs['data']['is_active']
        else:
            self.id = -1
            self.user_id = -1
            self.moderator_id = -1
            self.start_time = datetime.datetime.now()
            self.end_time = datetime.datetime.now()
            self.reason = 'empty reason'
            self.is_active = True

    def save(self):
        state, r = api_manager.post_data('temp-bans',
                                         user_id=str(self.user_id),
                                         moderator_id=str(self.moderator_id),
                                         start_time=self.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                                         end_time=self.end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                                         reason=self.reason,
                                         is_active=self.is_active)
        if state:
            self.id = r['id']

    def update(self):
        state, r = api_manager.edit_data('temp-bans',
                                         self.id,
                                         user_id=str(self.user_id),
                                         moderator_id=str(self.moderator_id),
                                         start_time=self.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                                         end_time=self.end_time.strftime('%Y-%m-%dT%H:%M:%S'),
                                         reason=self.reason,
                                         is_active=self.is_active)

    def delete(self):
        state, r = api_manager.delete_data('temp-bans',
                                           self.id)
