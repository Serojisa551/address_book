from django.urls import path
from .file_handler import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('contact/register/', register_contact, name='register_contact'),
    path('', contact_list, name='contact_list'),
    path('contact/<int:pk>/delete/', delete_contact, name='delete_contact'),
    path('contact/<int:pk>/details/', details_contact , name='details_contact'),
    path('contact/backup/', save_address_book , name='save_address_book'),
    path('contact/import/', import_address_book , name='import_address_book'),
    path('contact/<int:pk>/update/', update_contact, name='update_contact'),
    path('contact/search/', contact_search, name='search_contact'),
    path('register/', register_user, name='register_users'),
    path('login/', login_request, name="login_request"),
    path('logout/', logout_request, name='logout_request'),
    path('contact/delete/', delete_all_contact, name="delete_all_contact")
]
