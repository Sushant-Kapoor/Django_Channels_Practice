from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/sc/<str:groupName>/', consumers.MySyncConsumer.as_asgi()),
    path('ws/ac/<str:groupName>/', consumers.MyAsyncConsumer.as_asgi()),
]
