from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_contact, name='register_contact'),
    path('contact_list/', contact_list, name='contact_list'),
]
