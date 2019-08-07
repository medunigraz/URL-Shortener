from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import RedirectUrl


class RedirectUrlAdmin(GuardedModelAdmin):
    list_display = ('srcUrl', 'dstUrl')
    exclude = ['user']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(RedirectUrl, RedirectUrlAdmin)
