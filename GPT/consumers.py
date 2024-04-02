from django.db.models import Q
from helper.consumers import BaseAsyncJsonWebsocketConsumer
import uuid, base64

class ChatConsumer(BaseAsyncJsonWebsocketConsumer):

    async def connect(self):
        if await self.user_connect():
            self.query = None  
            self.request_key = None
            return await self.response(f"Hello {self.user.first_name}")
    

    async def receive_json(self, content, **kwargs):
        print(content)
        self.query = content['query']
        if 'file' in content and content['file']:
            await self.handle_file(content['file'])
        response = self.response_obj.get_response(self.query)
        await self.response(response)
     
    async def handle_file(self, file_info):
        if file_info:
            file_name = file_info.get('name', '')
            file_data = file_info.get('data', '')
            decoded_data = base64.b64decode(file_data)
            # print('decoded_data', decoded_data)
            with open(file_name, 'wb') as f:
                f.write(decoded_data)
    

    async def disconnect(self, close_code):
        pass
    
    async def response(self, gpt_response):
        data = {'response_id' : str(uuid.uuid4()), 'query' : self.query, 'request_key' : self.request_key, 'gpt_response' : gpt_response}
        await self.send_json(data)
        

            
        
        
        
