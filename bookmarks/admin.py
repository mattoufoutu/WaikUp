from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Link)
class LinkAdmin(admin.ModelAdmin):
    date_hierarchy = 'submit_date'
    list_display = ('url', 'title', 'author', 'submit_date', 'category', 'archived')


@admin.register(models.EMail)
class EMailAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.User, UserAdmin)
