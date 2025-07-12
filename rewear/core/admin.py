from django.contrib import admin
from .models import UserProfile, Item, SwapRequest

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')
    search_fields = ('user__username',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'status', 'uploader', 'created_at')
    list_filter = ('status', 'type')
    search_fields = ('title', 'category', 'tags')
    actions = ['mark_as_available', 'reject_items']

    def mark_as_available(self, request, queryset):
        updated = queryset.update(status='available')
        self.message_user(request, f"{updated} items marked as available.")

    def reject_items(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} items rejected.")

    mark_as_available.short_description = "Approve selected items"
    reject_items.short_description = "Reject selected items"

@admin.register(SwapRequest)
class SwapRequestAdmin(admin.ModelAdmin):
    list_display = ('item', 'requester', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('item__title', 'requester__username')
