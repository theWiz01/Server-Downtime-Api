from fastapi import APIRouter, Depends
from api.servers.schemas import ServerSchema
from database import get_session
from sqlmodel import Session
from api.auth.services import AuthService
from api.servers.services import ServerService
from typing import List
import requests

router = APIRouter()

@router.get('/')
def get_servers(session: Session = Depends(get_session), user_id = Depends(AuthService().auth_wrapper)):
    service = ServerService(session=session)
    servers = service.get_servers(user_id=user_id)
    return servers


@router.post('/')
def create_server(server : ServerSchema, session : Session = Depends(get_session), 
            user_id = Depends(AuthService().auth_wrapper)):
    service = ServerService(session=session)
    new_server = service.create_server(user_id=user_id, server=server)
    return new_server

@router.post('/ping/')
def ping_server(url:str):
    res = requests.get(url)
    return {'status_code' : res.status_code}


@router.put('/{server_id}')
def modify_server(server_id : str, server : ServerSchema, session : Session = Depends(get_session), 
                  user_id = Depends(AuthService().auth_wrapper)):
    service = ServerService(session=session)
    modified_server = service.modify_server(server_id=server_id, server=server)
    return modified_server


@router.delete('/{server_id}')
def delete_server(server_id : str, session : Session=Depends(get_session), user_id = Depends(AuthService().auth_wrapper)):
    service = ServerService(session=session)
    server = service.delete_server(server_id=server_id)
    return server
