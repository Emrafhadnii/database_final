from src.service_layer.message_bus import MessageBus
from config.settings import settings

messagebus = MessageBus(settings.RABBIT_URL)

async def get_message_bus():
    return messagebus
