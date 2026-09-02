from enum import Enum, IntEnum


class Status(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"
    
    
class Priority(IntEnum):
    LOW = 1
    MEDUIM = 2
    HIGH = 3
    