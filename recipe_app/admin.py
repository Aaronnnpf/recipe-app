from django.contrib import admin

from .models import Comment, Recipe


admin.site.register(Recipe)
admin.site.register(Comment)
