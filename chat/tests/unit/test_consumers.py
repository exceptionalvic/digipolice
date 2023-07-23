# tests/test_consumers.py

import json
import pytest
import asyncio
from channels.testing import WebsocketCommunicator
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.urls import reverse
from django.db import close_old_connections
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from chat.models import InfoMessage

User = get_user_model()

class FakeUserMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        scope['user'] = await self.get_fake_user()
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_fake_user(self):
        return User.objects.get_or_create(username="testuser")[0]

@pytest.mark.asyncio
@pytest.mark.django_db
async def test_chat_consumer():
    # Create a WebSocket communicator for the consumer
    communicator = WebsocketCommunicator(
        FakeUserMiddleware(
            "chat.consumers.ChatConsumer"
        ),
        "/ws/",
    )

    # Connect to the WebSocket
    connected = await communicator.connect()
    assert connected is True

    # Set up the payload
    payload = {
        'type': 'receive',
        'text': json.dumps({
            'message': 'Test Message',
        }),
    }

    # Send the payload to the consumer
    await communicator.send_json_to(payload)

    # Wait for the consumer to respond
    response = await communicator.receive_json_from()

    # Check if the response matches the expected format
    assert 'message' in response
    assert 'user' in response
    assert 'location' in response
    assert 'ip_address' in response

    # Disconnect from the WebSocket
    await communicator.disconnect()

    # Close the database connections (required for pytest-asyncio)
    await close_old_connections()
