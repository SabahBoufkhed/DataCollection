from django.contrib import admin

from .models import *

from import_export import resources
from import_export.admin import ExportMixin
from import_export.admin import ImportMixin

from import_export import fields


class ParticipantResource(resources.ModelResource):
    class Meta:
        model = Participant


@admin.register(Participant)
class ParticipantAdmin(ExportMixin, admin.ModelAdmin):
    fieldsets = [
        ('Basic', {'fields': ['first_name', 'last_name', 'current_phase']}),
        ('Experience', {'fields': ['position', 'type_experience', 'years_experience']}),
        ('More', {'fields': ['age', 'gender']})
    ]

    list_display = ('first_name', 'last_name', 'current_phase', 'date_added', 'id', 'user_url')

    resource_class = ParticipantResource
    pass

class ParticipantStatementResource(resources.ModelResource):
    author_full = fields.Field()

    class Meta:
        model = ParticipantStatement
        fields = ('timestamp', 'text', 'author_full')

    def dehydrate_author_full(self, p):
        return "%s %s" % (p.author.first_name, p.author.last_name)

@admin.register(ParticipantStatement)
class ParticipantStatementAdmin(ExportMixin, admin.ModelAdmin):
    fields = ['timestamp', 'text', 'author']
    list_display = ('timestamp', 'text', 'author')

    list_filter = ['author']

    resource_class = ParticipantStatementResource

#
# class ParticipantStatementAdmin(admin.ModelAdmin):
#     fields = ['timestamp', 'text', 'author']
#     list_display = ('timestamp', 'text', 'author')
#
#     list_filter = ['author']


class DistilledStatementResource(resources.ModelResource):
    class Meta:
        model = DistilledStatement
        fields = ('text_question', 'id')

@admin.register(DistilledStatement)
class DistilledStatementAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ('text_question', )

    resource_class = DistilledStatementResource


@admin.register(StatementSorting)
class StatementSortingAdmin(admin.ModelAdmin):
    list_display = ('participant', 'statement', 'order')

@admin.register(StatementRating)
class StatementRatingAdmin(admin.ModelAdmin):
    list_display = ('participant', 'statement', 'rating')

@admin.register(ModuleHeading)
class ModuleHeadingAdmin(admin.ModelAdmin):
    list_display = ('module_name',)

    fields = ('module_name', 'heading_content')
    readonly_fields = ('module_name',)
