from django.db import models
from django.contrib.auth.models import AbstractUser, User, Group, Permission

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    notes = models.TextField(max_length=256,blank=True, null=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        return self.name


# class CustomUser(AbstractUser):
#     
#     contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="Contact")
#     groups = models.ManyToManyField(Group, related_name="custom_users")
#     user_permissions = models.ManyToManyField(
#         Permission, related_name="custom_users"
#     )

