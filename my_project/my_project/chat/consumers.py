import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from datetime import datetime
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chatroom"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Gửi 50 tin nhắn gần nhất
        messages = await self.get_last_messages()
        await self.send(text_data=json.dumps({"messages": messages}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        username = data["username"]
        email = data["email"]
        avatar_url = data.get("avatar_url", "")
        message = data["message"]

        # Lưu tin nhắn vào database
        await self.save_message(username, email, avatar_url, message)

        # Gửi tin nhắn đến tất cả người dùng
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "username": username,
                "email": email,
                "avatar_url": avatar_url,
                "message": message,
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "username": event["username"],
                    "email": event["email"],
                    "avatar_url": event["avatar_url"],
                    "message": event["message"],
                }
            )
        )

    @database_sync_to_async
    def save_message(self, username, email, avatar_url, message):
        Message.objects.create(username=username, email=email, avatar_url=avatar_url, content=message)

    @database_sync_to_async
    def get_last_messages(self):
        messages = Message.objects.order_by("timestamp")[:50]
        return [
            {
                "username": msg.username,
                "email": msg.email,
                "avatar_url": msg.avatar_url,
                "message": msg.content,
                "timestamp": msg.timestamp.isoformat(),
            }
            for msg in messages
        ]
