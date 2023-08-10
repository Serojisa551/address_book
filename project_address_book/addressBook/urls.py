from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_contact, name='register_contact'),
    path('', contact_list, name='contact_list'),
    path('contact/<int:pk>/delete/', delete_contact, name='delete_contact'),
    path('contact/<int:pk>/details/', details_contact , name='details_contact'),
    path('contact/backup/', save_address_book , name='save_address_book'),

]
