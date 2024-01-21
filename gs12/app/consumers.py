from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


class MyWebsocketConsumer(WebsocketConsumer):
    def connect(self):
        print('Websocket connected...')
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        print('Message received from client...', text_data)
        self.send(text_data='Message sent from client')
        # self.close()
        # self.close(code=1423)

    def disconnect(self, code):
        print('Websocket disconnected...', code)


class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('Websocket connected...')
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        print('Message received from client...', text_data)
        await self.send(text_data='Message sent from client')
        # self.close()

    async def disconnect(self, code):
        print('Websocket disconnected...', code)
