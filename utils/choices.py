from enum import Enum

class ServerStatus(str, Enum):
    down = "Down"
    running = "Running"