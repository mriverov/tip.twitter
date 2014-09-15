from django.contrib import admin

# Register your models here.

from twitter.app.models import User
from twitter.app.models import Tweet

class TweetUserAdmin(admin.ModelAdmin):
	list_display = ('name','description')


admin.site.register(User,TweetUserAdmin)

class TweetTwitterAdmin(admin.ModelAdmin):
    list_display = ('tweet','description')

admin.site.register(Tweet,TweetTwitterAdmin)

