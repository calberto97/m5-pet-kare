from django.contrib import admin
from .models import Group


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at"]


admin.site.register(Group, ProfileAdmin)
