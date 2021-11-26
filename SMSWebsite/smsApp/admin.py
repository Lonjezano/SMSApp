from django.contrib import admin
from .models import *

admin.site.register(Recipient)
admin.site.register(RecipientGroup)
admin.site.register(SMS)
# Register your models here.
