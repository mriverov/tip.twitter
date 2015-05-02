from django.contrib import admin

# Register your models here.


from app.models import Domain, Topic, User, Tweet, Hashtag

class DomainAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Domain, DomainAdmin)