import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Group

class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group = await self.get_group_or_error(self.group_id)


        # Join the group channel
        await self.channel_layer.group_add(
            self.group.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group channel
        await self.channel_layer.group_discard(
            self.group.name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data['message']
        user = self.scope['user']

        # Create and save the message to the database
        message = Message.objects.create(
            user=user,
            group=self.group,
            content=message_content
        )

        # Send the message to the group
        await self.channel_layer.group_send(
            self.group.name,
            {
                'type': 'chat_message',
                'message': message_content,
                'username': user.username,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def get_group_or_error(self, group_id):
        try:
            group = Group.objects.get(id=group_id)
            if not self.scope['user'].groups.filter(id=group.id).exists():
                raise ValueError('You do not have permission to join this group.')
            return group
        except Group.DoesNotExist:
            raise ValueError('Group not found.')
