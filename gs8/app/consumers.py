from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('Websocket connected...', event)
        print('Channel layer...', self.channel_layer)  # default channel layer
        print('Channel name...', self.channel_name)  # default channel name

        # add channel to new or existing group
        # group_add is a async function which needs to be converted to sync
        async_to_sync(self.channel_layer.group_add)(
            'programmers', self.channel_name)

        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print('Message received from client...', event['text'])
        print('Type of message received from client', type(event['text']))
        async_to_sync(self.channel_layer.group_send)('programmers', {
            'type': 'chat.message',
            'message': event['text']
        })

    def chat_message(self, event):
        print('Event...', event)
        print('Actual data...', event['message'])
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    def websocket_disconnect(self, event):
        print('Websocket disconnected...', event)
        # Dicard channel from the group once it closes
        async_to_sync(self.channel_layer.group_discard)(
            'programmers', self.channel_name)
        raise StopConsumer()
