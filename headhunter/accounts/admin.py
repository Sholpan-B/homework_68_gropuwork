from django.contrib import admin
from accounts.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'phone')
    list_filter = ('username', 'email', 'role', 'phone')
    readonly_fields = ('id', 'date_joined')
    search_fields = ('email', 'username', 'role')
    fieldsets = (
        ('', {
            'fields': ('username', 'email', 'role', 'phone')
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
