from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    # Define the fields you want to display in the record data table
    list_display = ('username', 'email', 'phone_number', 'gender')  # Add the fields you want to display

# Register your model with the custom ModelAdmin
admin.site.register(CustomUser, CustomUserAdmin)
