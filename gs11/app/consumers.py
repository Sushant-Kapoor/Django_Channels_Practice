from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from .models import Chat, Group
import json
from channels.db import database_sync_to_async


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('Websocket connected...', event)
        print('Channel layer...', self.channel_layer)  # default channel layer
        print('Channel name...', self.channel_name)  # default channel name

        self.group_name = self.scope['url_route']['kwargs']['groupName']
        print('Groupname in consumer...', self.group_name)

        # add channel to new or existing group
        # group_add is a async function which needs to be converted to sync
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name)

        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print('Message received from client...', event['text'])
        print('Type of message received from client', type(event['text']))
        data = json.loads(event['text'])

        # Get Group object, to find where to save chats
        group = Group.objects.get(name=self.group_name)
        print("Data", data)
        print("Type of Data", type(data))
        data['user'] = self.scope['user'].username
        if self.scope['user'].is_authenticated:
            # Create new chat object
            chat = Chat(
                content=data['msg'],
                group=group
            )

            chat.save()
            async_to_sync(self.channel_layer.group_send)(self.group_name, {
                'type': 'chat.message',
                'message': json.dumps(data)
            })
        else:
            self.send({
                'type': 'websocket.send',
                'text': json.dumps({"msg": "Login required", "user": "Guest User"})
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
            self.group_name, self.channel_name)
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('Websocket connected...', event)
        print('Channel layer...', self.channel_layer)  # default channel layer
        print('Channel name...', self.channel_name)  # default channel name
        self.group_name = self.scope['url_route']['kwargs']['groupName']

        # add channel to new or existing group
        # group_add is a async function which needs to be converted to sync
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('Message received from client...', event['text'])
        print('Type of message received from client', type(event['text']))

        data = json.loads(event['text'])

        # Get Group object, to find where to save chats
        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        data['user'] = self.scope['user'].username

        if self.scope['user'].is_authenticated:
            # Create new chat object
            chat = Chat(
                content=data['msg'],
                group=group
            )

            await database_sync_to_async(chat.save)()
            await self.channel_layer.group_send(self.group_name, {
                'type': 'chat.message',
                'message': json.dumps(data)
            })
        else:
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({"msg": "Login required", "user": "Guest User"})
            })

    async def chat_message(self, event):
        print('Event...', event)
        print('Actual data...', event['message'])
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    async def websocket_disconnect(self, event):
        print('Websocket disconnected...', event)
        # Dicard channel from the group once it closes
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name)
        raise StopConsumer()
