from django.contrib import admin

# Register your models here.


from mole.app.models import Domain, Topic, Hashtag

class DomainAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Domain, DomainAdmin)