import json, socket
import urllib.request, urllib.parse, urllib.error
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import InfoMessage
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model


User = get_user_model()

# try to get the hostname and Ip of where
host_name = socket.gethostname() 
get_host_ip = socket.gethostbyname(host_name) 
host_ip = '51.89.232.89'
# # serviceurl = 'http://www.geoplugin.net/json.gp?ip='+host_ip
serviceurl = 'http://ip-api.com/json/'+host_ip

print('Retrieving', serviceurl)
uh = urllib.request.urlopen(serviceurl)
data = uh.read().decode()
# print('Retrieved', len(data), 'characters')
js = json.loads(data)
# print(js)
# print(data.city)
# print(js['regionName'])
print(js)

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.roomGroupName = "group_chat_gfg"
#         await self.channel_layer.group_add(
#             self.roomGroupName ,
#             self.channel_name
#         )
#         await self.accept()
#     async def disconnect(self , close_code):
#         await self.channel_layer.group_discard(
#             self.roomGroupName ,
#             self.channel_layer
#         )
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         username = text_data_json["username"]
#         await self.channel_layer.group_send(
#             self.roomGroupName,{
#                 "type" : "sendMessage" ,
#                 "message" : message ,
#                 "username" : username ,
#             })
#     async def sendMessage(self , event) :
#         message = event["message"]
#         username = event["username"]
#         await self.send(text_data = json.dumps({"message":message ,"username":username}))

# chat_app/consumers.py




class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_room'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Authenticate the user for WebSocket connections
        await self.authenticate_user()
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        location = js['city'],
        ip_address= str(get_host_ip),
        user = self.scope['user'].username
        
        try:
            # Save the message and sender's username to the database
            await self.save_message(user, message)
        except Exception as e:
            # Handle any exceptions during message saving
            print(str(e))

        # Send message to the intelligence message board group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user':user,
                'location': location,
                'ip_address': ip_address,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user= event['user']
        location = event['location'],
        ip_address= event['ip_address'],

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'location': location,
            'ip_address': ip_address,
            
        }))
        
    @database_sync_to_async
    def authenticate_user(self):
        # Check if the user is authenticated and add the user to the scope if they are
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            self.close()
        return user
    
    @database_sync_to_async
    def save_message(self, user, message):
        try:
            new_message = InfoMessage(
                                username=str(user), 
                                content=message, 
                                ip_address=str(get_host_ip),
                                location=js['city'])
            new_message.save()
            print('message saved: %s' % new_message.content)
        except Exception as e:
            new_message = InfoMessage(
                                username=str(user), 
                                content=message, 
                                ip_address=str(get_host_ip),
                                )
            new_message.save()
            print(f"An error occurred while saving the message with location: {e}")