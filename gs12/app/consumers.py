from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


class MyWebsocketConsumer(WebsocketConsumer):
    def connect(self):
        print('Websocket connected...')

    def receive(self, text_data=None, bytes_data=None):
        print('Message received from client...', text_data)

    def disconnect(self, code):
        print('Websocket disconnected...', code)
