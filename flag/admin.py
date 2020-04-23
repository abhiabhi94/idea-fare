from django.contrib import admin

from flag.models import FlaggedContent, FlagInstance

class InlineFlagInstance(admin.TabularInline):
    model = FlagInstance
    extra = 0
    readonly_fields = ['flagged_content', 'user', 'date_flagged', 'reason', 'comment']

class FlaggedContentAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'creator', 'status', 'moderator', 'count']
    readonly_fields = ['content_object', 'creator', 'count']
    exclude = ['content_type', 'object_id']
    search_fields = ['content_object']
    inlines = [InlineFlagInstance]

admin.site.register(FlaggedContent, FlaggedContentAdmin)
