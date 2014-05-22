from django.contrib import admin

# Register your models here.

from app.models import TweetUser

class TweetUserAdmin(admin.ModelAdmin):
	list_display = ('name','description')


admin.site.register(TweetUser,TweetUserAdmin)

