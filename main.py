from config import settings
from core.handler import Handler

if __name__ == '__main__':
    message_kind = settings.message_kind
    message_kind_handler = getattr(Handler, message_kind)
    message_kind_handler()


