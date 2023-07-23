from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
       class Meta:
           model = Message
           fields = ('id', 'username', 'content','ip_address','location', 'timestamp')
           read_only_fields = ('id', 'timestamp','ip_address')