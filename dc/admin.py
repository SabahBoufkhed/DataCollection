from django.contrib import admin

from .models import *

from import_export import resources
from import_export.admin import ExportMixin
from import_export.admin import ImportMixin
from import_export.admin import ImportExportMixin

from import_export import fields

from django import template

@admin.register(Participant)
class ParticipantAdmin(ImportExportMixin, admin.ModelAdmin):
    class ParticipantResource(resources.ModelResource):
        class Meta:
            model = Participant
            fields = ('first_name', 'last_name', 'email', 'age', 'gender', 'type_experience', 'years_experience', 'discipline')

        def get_instance(self, instance_loader, row):
            return False

        def init_instance(self, row=None):
            o = self._meta.model()
            o.id = str(uuid.uuid4())
            return o

        def before_import(self, dataset, dry_run, **kwargs):
            if 'id' not in dataset.headers:
                dataset.headers.append('id')

    readonly_fields = ('user_url', 'user_email_message')
    def user_email_message(self, instance):
        t = template.Template(ModuleHeading.objects.get(module_name='user_email_template').heading_content)
        c = Context({
            'full_name': str(instance),
            'user_url': instance.user_url(),
            'user_password': instance.password
        })

        return t.render(c)

    user_email_message.short_description = "Email template ..."

    fieldsets = [
        ('Basic', {'fields': ['first_name', 'last_name', 'current_phase', 'password']}),
        ('Experience', {'fields': ['position', 'type_experience', 'years_experience']}),
        ('More', {'fields': ['age', 'gender']}),
        ('Email', {'fields': ['email', 'user_url', 'user_email_message']})
    ]

    list_editable = ('current_phase',)
    list_display = ('first_name', 'last_name', 'current_phase', 'date_added', 'id', 'password', 'user_url')

    resource_class = ParticipantResource


@admin.register(ParticipantStatement)
class ParticipantStatementAdmin(ExportMixin, admin.ModelAdmin):
    class ParticipantStatementResource(resources.ModelResource):
        author_full = fields.Field()

        class Meta:
            model = ParticipantStatement
            fields = ('timestamp', 'text', 'author_full')

        def dehydrate_author_full(self, p):
            return "%s %s" % (p.author.first_name, p.author.last_name)

    fields = ['timestamp', 'text', 'author']
    list_display = ('timestamp', 'text', 'author')

    list_filter = ['author']

    resource_class = ParticipantStatementResource



@admin.register(DistilledStatement)
class DistilledStatementAdmin(ImportMixin, admin.ModelAdmin):
    class DistilledStatementResource(resources.ModelResource):
        class Meta:
            model = DistilledStatement
            fields = ('text_question',)

        def get_instance(self, instance_loader, row):
            return False

        def init_instance(self, row=None):
            o = self._meta.model()
            return o

    list_display = ('text_question', )

    resource_class = DistilledStatementResource


@admin.register(StatementSorting)
class StatementSortingAdmin(ExportMixin, admin.ModelAdmin):
    class StatementSortingResource(resources.ModelResource):
        author_full_name = fields.Field()
        statement_text = fields.Field()

        class Meta:
            model = StatementSorting
            fields = ('author_full_name', 'statement_text', 'order')

        def dehydrate_author_full_name(self, p):
            return "%s %s" % (p.author.first_name, p.author.last_name)

        def dehydrate_statement_text(self, s):
            return str(s.statement)


    list_display = ('author', 'statement', 'order')
    resource_class = StatementSortingResource


@admin.register(StatementRating)
class StatementRatingAdmin(ExportMixin, admin.ModelAdmin):
    class StatementRatingResource(resources.ModelResource):
        author_full_name = fields.Field()
        statement_text = fields.Field()

        class Meta:
            model = StatementRating
            fields = ('author_full_name', 'statement_text', 'rating')

        def dehydrate_author_full_name(self, p):
            return "%s %s" % (p.author.first_name, p.author.last_name)

        def dehydrate_statement_text(self, s):
            return str(s.statement)

    list_display = ('author', 'statement', 'rating')
    resource_class = StatementRatingResource


@admin.register(ModuleHeading)
class ModuleHeadingAdmin(admin.ModelAdmin):
    list_display = ('module_name',)

    fields = ('module_name', 'heading_content')
    #readonly_fields = ('module_name',)
