from config import settings
from core.handler import Handler

if __name__ == '__main__':
    operation_kind = settings.operation_kind
    handler = getattr(Handler, operation_kind)
    handler()
