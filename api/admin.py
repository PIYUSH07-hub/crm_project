from django.contrib import admin
from .models import Client, Project
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

# --- Client Admin ---
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'created_by', 'created_at')
    search_fields = ('client_name',)
    readonly_fields = ('created_at', 'updated_at', 'created_by')


# --- Project Admin ---
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_name', 'get_clients', 'get_users', 'created_by', 'created_at')
    search_fields = ('project_name',)
    filter_horizontal = ('clients', 'users')  # For selecting many-to-many fields

    def get_clients(self, obj):
        return ", ".join([client.client_name for client in obj.clients.all()])
    get_clients.short_description = 'Clients'

    def get_users(self, obj):
        return ", ".join([user.username for user in obj.users.all()])
    get_users.short_description = 'Users'


# --- Custom User Admin to show ID ---
class CustomUserAdmin(DefaultUserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active')
    search_fields = ('id', 'username', 'email')

# Unregister and re-register User admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
