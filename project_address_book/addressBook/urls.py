from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_contact, name='register_contact'),
    path('', contact_list, name='contact_list'),
    path('contact/<int:pk>/delete/', delete_contact, name='delete_contact'),
    path('contact/<int:pk>/details/', details_contact , name='details_contact'),
<<<<<<< HEAD
    path('contact/backup/', save_address_book , name='save_address_book'),
    path('contact/import/', import_address_book , name='import_address_book'),
=======
>>>>>>> origin/develop
    path('contact/<int:pk>/update/', update_contact, name='update_contact'),
    path('contact/<query>/search/', contact_search, name='search_contact'),
]
