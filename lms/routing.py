from django.urls import path
from .consumers import ChatConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/<str:room_name>/', ChatConsumer),
    ])