from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    notes = models.TextField(max_length=256,blank=True, null=True)


    def __str__(self):
        return self.name
