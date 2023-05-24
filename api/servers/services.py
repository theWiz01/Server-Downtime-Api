from fastapi import Depends
from sqlmodel import Session, select
from database import get_session
from api.servers.schemas import ServerSchema
from models.server import Server
from utils.funcs import exception_message

class ServerService:
    def __init__(self, session : Session = Depends(get_session)):
        self.session = session

    def create_server(self, user_id : str, server : ServerSchema):
        new_server = Server(**server.dict())
        new_server.user_id = user_id
        self.session.add(new_server)
        self.session.commit()
        self.session.refresh(new_server)
        return new_server
    
    def get_servers(self, user_id : str):
        statement = select(Server).where(Server.user_id == user_id)
        servers = self.session.execute(statement).scalars().all()
        return servers
    
    def modify_server(self, server_id : str, server : ServerSchema):
        statement = select(Server).where(Server.id == server_id)
        data = self.session.exec(statement).one()
        if data :
            data.name = server.name or data.name
            data.url = server.url or data.url
            self.session.add(data) 
            self.session.commit()
            self.session.refresh(data)
            return data
        raise exception_message(status_code=404, message="Server Not Found")

    def delete_server(self, server_id):
        statement = select(Server).where(Server.id == server_id)
        server = self.session.exec(statement).one()
        if server:
            self.session.delete(server)
            self.session.commit() 
            return {"message" : "Server Deleted Successfully"}
        raise exception_message(status_code=404, message="Server Not Found")
