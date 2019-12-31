import yaml

from src.utils.api_manager import APIManager

with open("run/config/config.yml", 'r') as stream:
    data = yaml.safe_load(stream)
    api_manager = APIManager(
        data['api']['url'],
        data['api']['token']
    )


class CustomCommand:
    id: int
    trigger: str
    message: str
    is_active: bool

    def __init__(self, **kwargs):
        """
        Init of the class
        :param kwargs: a warn from the api
        """
        if 'data' in kwargs:
            self.id = int(kwargs['data']['id'])
            self.trigger = kwargs['data']['user_id']
            self.message = kwargs['data']['message']
            self.is_active = kwargs['data']['is_active']
        else:
            self.id = -1
            self.trigger = "command"
            self.message = "message"
            self.is_active = True

    def save(self):
        state, r = api_manager.post_data('custom-commands',
                                         trigger=self.trigger,
                                         message=self.message,
                                         is_active=self.is_active)
        if state:
            self.id = r['id']

    def update(self):
        state, r = api_manager.edit_data('custom-commands',
                                         self.id,
                                         trigger=self.trigger,
                                         message=self.message,
                                         is_active=self.is_active)

    def delete(self):
        state, r = api_manager.delete_data('custom-commands',
                                           self.id)
