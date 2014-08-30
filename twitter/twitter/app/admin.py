from django.contrib import admin

# Register your models here.

from app.models import TweetUser
from app.models import Tweet

class TweetUserAdmin(admin.ModelAdmin):
	list_display = ('name','description')


admin.site.register(TweetUser,TweetUserAdmin)

class TweetTwitterAdmin(admin.ModelAdmin):
    list_display = ('tweet','description')

admin.site.register(Tweet,TweetTwitterAdmin)

