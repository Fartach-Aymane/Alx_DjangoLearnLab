from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'actor', 'verb', 'timestamp', 'read')
    list_filter = ('timestamp', 'read', 'recipient')
    search_fields = ('actor__username', 'recipient__username', 'verb')
    readonly_fields = ('timestamp',)