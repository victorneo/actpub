from enum import Enum


class ActivityTypes(Enum):
    ACCEPT = 'Accept'
    FOLLOW = 'Follow'
    CREATE = 'Create'
    UNDO = 'Undo'