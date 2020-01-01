import yaml

from src.utils.api_manager import APIManager

with open("run/config/config.yml", 'r') as stream:
    data = yaml.safe_load(stream)
    api_manager = APIManager(
        data['api']['url'],
        data['api']['token']
    )


class Role:
    id: int
    slug: str
    role_id: int

    def __init__(self, **kwargs):
        """
        Init of the class
        :param kwargs: a warn from the api
        """
        if 'data' in kwargs:
            self.id = int(kwargs['data']['id'])
            self.slug = kwargs['data']['slug']
            self.role_id = int(kwargs['data']['role_id'])
        else:
            self.id = -1
            self.slug = "command"
            self.role_id = -1

    def save(self):
        state, r = api_manager.post_data('roles',
                                         slug=self.slug,
                                         role_id=str(self.role_id))

        if state:
            self.id = r['id']

    def update(self):
        state, r = api_manager.edit_data('roles',
                                         self.id,
                                         slug=self.slug,
                                         role_id=str(self.role_id))

    def delete(self):
        state, r = api_manager.delete_data('roles',
                                           self.id)
