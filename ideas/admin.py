from django.contrib import admin

from ideas.models import Idea


class IdeaAdmin(admin.ModelAdmin):
    readonly_fields = ['slug', 'date_created', 'date_updated']
    list_display = ['title', 'conceiver', 'date_created',
                    'date_created', 'visibility', 'date_updated']
    search_fields = ['conceiver__username', 'slug', ]

    list_filter = ['visibility', ]

admin.site.register(Idea, IdeaAdmin)

