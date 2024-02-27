from django.contrib import admin
from alert.models import Alert


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["asset", "price", "track_type", "status", "created", ]


admin.site.register(Alert, AuthorAdmin)
