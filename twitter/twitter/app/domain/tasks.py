import tweepy
import requests
from twitter.app.models import User

#from celery.task.base import periodic_task
#from celery.schedules import crontab

class Scheduler():
	
	def __init__(self, _autenticator):
		self.autenticator = _autenticator
		self.auth = self.autenticator.authenticate()
		self.api = tweepy.API(self.auth)
		self.current_cursor = -1
		
	def resetCursor(self):
		self.current_cursor = -1
		
	#@periodic_task(run_every=crontab(minute="*/18"))
	def processFollowersFrom(self, user, user_persistor):
		oauth = self.autenticator.get_oauth()
		api_path = "https://api.twitter.com/1.1/followers/ids.json?screen_name="+user.screen_name
		try:
			if self.current_cursor!=0:
				url_with_cursor = api_path + "&cursor=" + str(self.current_cursor)
				response = requests.get(url=url_with_cursor, auth=oauth)
				response_dictionary = response.json()
				self.current_cursor = response_dictionary['next_cursor']
				followers_ids = response_dictionary['ids']
				self.saveFollowersDispacher(user, followers_ids, user_persistor)
			
			if self.current_cursor==0:
				self.resetCursor
				return
				#cancel task
		except tweepy.error.TweepError:
			print "Followers process has been suspended, waiting for permission from "+user.screen_name


	def saveFollowersDispacher(self, user, followers, user_persistor):
		dividedFollowers = [followers[x:x+299] for x in xrange(1, len(followers), 299)]
		for f in dividedFollowers:
			#start this task
			print "start saving followers"
			self.saveFollowers(user, f, user_persistor)
			break
	
	#@periodic_task(run_every=crontab(minute="*/18"))	
	def saveFollowers(self, user, followers, user_persistor):
		for i in followers:
			follower = self.api.get_user(i)
			print "saving user "+ str(i)
			try:
				follower = User.objects.get(id = follower.id)
			except User.DoesNotExist:
				follower = user_persistor.saveUserFromApi(follower)
			user.followers.add(follower)
			print "finishing saving user "+ str(i)

			
				
		
		
"""	

			
	#@periodic_task(run_every=crontab(minute="*/10"))
	def digger(self, count=50):
		print "Start Digger on " +time.strftime("%d/%m/%Y") + " at " +time.strftime("%H:%M:%S")
		a = Authenticator()
		d = Digger(a.authenticate())
		#d.topic.saveConfiguration("Deporte","premierLeague")
		#d.start = datetime.datetime.now().replace(microsecond=0)
		#d.startStreaming()
		
		print "End Digger on " +time.strftime("%d/%m/%Y") + " at " +time.strftime("%H:%M:%S")
		return "Finished"
"""

	


