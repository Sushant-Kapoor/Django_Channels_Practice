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
        print('Message received from client...', event)
        self.send({
            'type': 'websocket.send',
            'text': 'This is from server to client'
        })

    def websocket_disconnect(self, event):
        print('Websocket disconnected...', event)
        # Dicard channel from the group once it closes
        async_to_sync(self.channel_layer.group_discard)(
            'programmers', self.channel_name)
        raise StopConsumer()
