from django.db import models
from django.urls import reverse


class RecipientGroup(models.Model):
    group_name = models.CharField(max_length=30, default='General contacts')

    def __str__(self):
        return self.group_name


class Recipient(models.Model):
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    phone_number = models.CharField(max_length=13, blank=False, null=False)
    group_name = models.ForeignKey(RecipientGroup, default=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.phone_number

    def get_absolute_url(self):
        return reverse('sms-home')


class SMS(models.Model):
    phone_number = models.CharField(max_length=16)
    group_name = models.ForeignKey(RecipientGroup, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    cost = models.CharField(max_length=13, default='MWK 0.0000')
    status = models.CharField(max_length=10, blank=True, null=True)
    statusCode = models.IntegerField(blank=True, default=200)

    def __str__(self):
        return self.phone_number
