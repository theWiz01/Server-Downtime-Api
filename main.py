from fastapi import FastAPI, Depends
from router import router
from database import create_db_and_tables, get_session
import asyncio
from utils.funcs import all_servers
import threading


def get_app():
    app = FastAPI(
        title= 'Server Downtime Monitor',
        description= 'Monitor you server downtime',
    )
    app.include_router(router, prefix='/api')

    @app.on_event('startup')
    def schedule_ping():
        cron = threading.Thread(target=all_servers)
        cron.start()

    return app