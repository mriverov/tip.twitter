from django.contrib import admin

# Register your models here.
from mole.app.models import KeyWord


class DomainAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(KeyWord, DomainAdmin)