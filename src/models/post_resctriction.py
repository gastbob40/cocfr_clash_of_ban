import datetime
import yaml
from src.utils.api_manager import APIManager

with open("run/config/config.yml", 'r') as stream:
    data = yaml.safe_load(stream)
    api_manager = APIManager(
        data['api']['url'],
        data['api']['token']
    )


class PostRestriction:
    id: int
    user_id: int
    channel_id: int
    start_time: datetime.date
    end_time: datetime.date

    def __init__(self, **kwargs):
        """
        Init of the class
        :param kwargs: a warn from the api
        """
        if 'data' in kwargs:
            self.id = int(kwargs['data']['id'])
            self.user_id = int(kwargs['data']['user_id'])
            self.channel_id = int(kwargs['data']['channel_id'])
            self.start_time = datetime.datetime.strptime(kwargs['data']['start_time'], '%Y-%m-%dT%H:%M:%S')
            self.end_time = datetime.datetime.strptime(kwargs['data']['end_time'], '%Y-%m-%dT%H:%M:%S')
        else:
            self.id = -1
            self.user_id = -1
            self.channel_id = -1
            self.start_time = datetime.datetime.now()
            self.end_time = datetime.datetime.now()

    def save(self):
        state, r = api_manager.post_data('post-restrictions',
                                         user_id=str(self.user_id),
                                         channel_id=str(self.channel_id),
                                         start_time=self.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                                         end_time=self.end_time.strftime('%Y-%m-%dT%H:%M:%S'))
        if state:
            self.id = r['id']

    def update(self):
        state, r = api_manager.edit_data('post-restrictions',
                                         self.id,
                                         user_id=str(self.user_id),
                                         channel_id=str(self.channel_id),
                                         start_time=self.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
                                         end_time=self.end_time.strftime('%Y-%m-%dT%H:%M:%S'))

    def delete(self):
        state, r = api_manager.delete_data('post-restrictions',
                                           self.id)
