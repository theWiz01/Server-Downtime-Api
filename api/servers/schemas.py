from pydantic import BaseModel
from uuid import UUID

class ServerSchema(BaseModel):
    # user_id : UUID
    name : str
    url : str