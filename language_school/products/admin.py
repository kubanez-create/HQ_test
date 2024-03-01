from django.contrib import admin

from .models import Group, Lesson, Product
from users.models import CustomUser

admin.site.register(Group)
admin.site.register(Lesson)
admin.site.register(Product)
admin.site.register(CustomUser)
