from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref import async_to_sync


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

    def websocket_disconnect(self, event):
        print('Websocket disconnected...', event)
        raise StopConsumer()
