from fastapi import HTTPException
from sqlmodel import Session, select
from models.server import Server
from database import engine, get_session
import requests
import time, concurrent.futures

def exception_message(status_code, message):
    return HTTPException(status_code=status_code, detail=message) 

def ping_server(url : str):
    res = requests.get(url)
    return res.status_code

def modify_server_status(server):
    modified = False
    try:
        status_code = ping_server(server.url)
        if status_code in range(500, 512):
            if server.active or server.active is None:
                server.active = False
                modified = True
        else:
            if not server.active or server.active is None:
                server.active = True
                modified = True
    except Exception as e:
        print(f'Error : {e}')
    if modified:
        with Session(engine) as session:
            # session.close()
            session.add(server)
            session.commit()
            print('update made')
            # session.refresh(server)
    return True

def all_servers():
    # while True:
    servers = []
    with Session(engine) as session:
        servers = session.execute(select(Server)).scalars().all()
        session.close()
    print(servers, 'sssss')
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(servers)) as executor:
        executor.map(modify_server_status, servers)
        
        # session.close()
            
        # time.sleep(300)

