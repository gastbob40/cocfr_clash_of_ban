import datetime

import yaml

from src.utils.api_manager import APIManager

with open("run/config/config.yml", 'r') as stream:
    data = yaml.safe_load(stream)
    api_manager = APIManager(
        data['api']['url'],
        data['api']['token']
    )


class Donation:
    id: int
    user_id: int
    amount: int
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
            self.amount = int(kwargs['data']['amount'])
            self.start_time = datetime.datetime.strptime(kwargs['data']['start_time'], '%Y-%m-%dT%H:%M:%SZ')
            self.end_time = datetime.datetime.strptime(kwargs['data']['end_time'], '%Y-%m-%dT%H:%M:%SZ')
            self.is_active = kwargs['data']['is_active']
        else:
            self.id = -1
            self.user_id = -1
            self.amount = -1
            self.start_time = datetime.datetime.now()
            self.end_time = datetime.datetime.now()
            self.is_active = True

    def save(self):
        state, r = api_manager.post_data('donations',
                                         user_id=str(self.user_id),
                                         amount=self.amount,
                                         start_time=self.start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                                         end_time=self.end_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                                         is_active=self.is_active)
        if state:
            self.id = r['id']

    def update(self):
        state, r = api_manager.edit_data('donations',
                                         self.id,
                                         user_id=str(self.user_id),
                                         amount=self.amount,
                                         start_time=self.start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                                         end_time=self.end_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                                         is_active=self.is_active)

    def delete(self):
        state, r = api_manager.delete_data('donations',
                                           self.id)
