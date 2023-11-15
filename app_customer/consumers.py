# accounts/consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from . import models

class NewUserConsumer(WebsocketConsumer):
	def connect(self):
		user = self.scope['user']
		models.CustomerModel.objects.filter(user=user).update(online=True)
		async_to_sync(self.channel_layer.group_add)("online", self.channel_name)

		self.accept()

		async_to_sync(self.channel_layer.group_send)(
            "online",
            {
                "type": "online_status",
                "text": {
					'user': user.id,
					'online':True
				},
            },
        )
		
	def disconnect(self, close_code):
		user = self.scope['user']
		models.CustomerModel.objects.filter(user=user).update(online=False)
		async_to_sync(self.channel_layer.group_discard)('online', self.channel_name)
		async_to_sync(self.channel_layer.group_send)(
            "online",
            {
                "type": "online_status",
                "text": {
					'user': user.id,
					'online':False
				},
            },
        )

	def online_status(self, event):
		self.send(text_data=json.dumps(event['text']))