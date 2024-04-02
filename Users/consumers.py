from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from rest_framework_simplejwt.tokens import  RefreshToken
from channels.db import database_sync_to_async
import re
import uuid
from Users.models import User
    

class UserLoginRegister(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        self.email = None
        self.password = None      
        self.user = None
        self.query = None  
        self.request_key = 'email'
        return await self.response('Please enter your email address...')
    

    async def receive_json(self, content, **kwargs):
        self.query = content['query']
        if self.request_key == 'email':
            email = await self.extract_email(content['query'])
            if email is None:
                return await self.response('In your answer there is no email address')
            self.email = email
            self.request_key = 'password'
            return await self.response('Please enter your password as well as...')
        elif self.request_key == 'password':
            password = content['query']
            self.password = password
            return await self.login_or_register()
        elif self.request_key == 'register':
            confimation = content['query']
            if confimation == 'yes':
                await self.user_register()
            else:
                self.request_key = 'email'
                await self.response('Please enter your email address...')
        elif self.request_key == 'name':
            name = content['query']
            await self.set_user_name(name)
            return await self.login_or_register()


    async def disconnect(self, close_code):
        pass
    
    async def response(self, gpt_response):
        data = {'response_id' : str(uuid.uuid4()), 'query' : self.query, 'request_key' : self.request_key, 'gpt_response' : gpt_response}
        await self.send_json(data)
        

    async def extract_email(self, query):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, query)
        
        if match:
            email = match.group()
            return email
        else:
            return None

    @database_sync_to_async
    def authenticate(self):
        try:
            user = User.objects.get(email=self.email)
            if check_password(self.password, user.password):
                self.user = user
                return True, True
            else:
                return True, False
        except User.DoesNotExist:
            return False, False

    @database_sync_to_async
    def get_tokens_for_user(self):
        refresh = RefreshToken.for_user(self.user)
        return {
            'token': str(refresh.access_token),
            'name' : self.user.first_name 
        }
   
    @database_sync_to_async
    def set_user_name(self, name):
        self.user.first_name = name
        self.user.save()
   
    @database_sync_to_async
    def user_create(self):
        user = User.objects.create_user(email=self.email, password=self.password)
        self.user = user
        
    async def user_register(self):
        user = await self.user_create()
        await self.login_or_register()

        
    async def login_or_register(self):
        email, password = await self.authenticate()
        if email and password:
            self.request_key = 'token'
            if self.user.first_name:
                await self.response(await self.get_tokens_for_user())
            else:
                self.request_key = 'name'
                await self.response('Please enter your Name')
        elif email and not password:
            await self.response('Invalid password provided please re type your correct password')
        else:
            self.request_key = 'register'
            await self.response('Credentials not found do you want to registed them')
            
                  

            
        
        
        
