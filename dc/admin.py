from django.contrib import admin

from .models import *

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic', {'fields': ['first_name', 'last_name', 'password']}),
        ('Experience', {'fields': ['type_experience', 'years_experience']}),
        ('More', {'fields': ['age', 'gender']})
    ]

    list_display = ('first_name', 'last_name', 'years_experience', 'date_added', 'password', 'id', 'user_url')


class ParticipantStatementAdmin(admin.ModelAdmin):
    fields = ['timestamp', 'text', 'author']
    list_display = ('timestamp', 'text', 'author')

    list_filter = ['author']


class StatementSortingAdmin(admin.ModelAdmin):
    list_display = ('participant', 'statement', 'order')


class StatementRatingAdmin(admin.ModelAdmin):
    list_display = ('participant', 'statement', 'rating')


class ModuleHeadingAdmin(admin.ModelAdmin):
    list_display = ('module_name',)

    fields = ('module_name', 'heading_content')
    readonly_fields = ('module_name',)

    #actions = None

    #def has_add_permission(self, request):
    #    return False

admin.site.register(ParticipantStatement, ParticipantStatementAdmin)

admin.site.register(DistilledStatement)
admin.site.register(StatementSorting, StatementSortingAdmin)
admin.site.register(StatementRating, StatementRatingAdmin)

admin.site.register(ModuleHeading, ModuleHeadingAdmin)