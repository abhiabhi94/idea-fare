from django.contrib import admin

from ideas.models import Idea, IdeaComment


class IdeaAdmin(admin.ModelAdmin):
    readonly_fields = ['slug', 'date_created', 'date_updated']
    list_display = ['title', 'conceiver', 'date_created',
                    'date_created', 'visibility', 'date_updated']
    search_fields = ['conceiver__username', 'slug', ]

    list_filter = ['visibility', ]

class IdeaCommentAdmin(admin.ModelAdmin):
    readonly_fields = ['flag']
    list_display = ['comment']


admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaComment, IdeaCommentAdmin)

