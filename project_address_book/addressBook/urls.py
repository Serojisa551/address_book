from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_contact, name='register_contact'),
    path('', contact_list, name='contact_list'),
    path('contact/<int:pk>/delete/', delete_contact, name='delete_contact'),
    path('contact/<int:pk>/details/', details_contact , name='details_contact'),
    path('contact/<int:pk>/update/', update_contact, name='update_contact'),
    path('contact/<query>/search/', contact_search, name='search_contact'),
]
