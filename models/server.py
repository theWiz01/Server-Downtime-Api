from utils.models import IDTimeBasedModel
from uuid import UUID

class Server(IDTimeBasedModel, table=True):
    __tablename__ = 'servers'

    user_id : UUID
    url : str
    name : str
    active : bool = True

    def __repr__(self):
        return f'{self.name}'

