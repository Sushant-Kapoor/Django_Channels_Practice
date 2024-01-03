# Topic - Consumer
from channels.consumer import SyncConsumer, AsyncConsumer

class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self, event):
        print('Web socket connected...')

    def websocket_receive(self, event):
        print('Message received...')

    def websocket_disconnect(self, event):
        print('Websocket disconnect...')
    

class MyAsyncConsumer(SyncConsumer):
    
    async def websocket_connect(self, event):
        print('Web socket connected...')

    async def websocket_receive(self, event):
        print('Message received...')

    async def websocket_disconnect(self, event):
        print('Websocket disconnect...')

