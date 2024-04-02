from django.urls import path
from Users.consumers import UserLoginRegister
from GPT.consumers import ChatConsumer

urlpatterns = []

ws_urlpatterns = [
    path('ws/register-login', UserLoginRegister.as_asgi()),
    path('ws/chat', ChatConsumer.as_asgi())
]