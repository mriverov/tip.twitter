import tweepy
from authenticator import Authenticator

class UserTest():

    def __init__(self):
        authenticator = Authenticator()
        auth = authenticator.authenticate()
        self.api = tweepy.API(auth)

    def dowloandFollowers(self):
        count = 0
        current_cursor = ""
        try:
            for page in tweepy.Cursor(self.api.followers, screen_name="marley_ok").pages():
                #current_cursor = cursor.iterator.next_cursor
                print "****** PAGE: " + repr(page)
                cursor = tweepy.Cursor(self.api.followers, screen_name="marley_ok", cursor =  current_cursor)
                ids = self.api.followers(screen_name="marley_ok", cursor = current_cursor)
                current_cursor = cursor.iterator.next_cursor
                count += len(ids)
                print "****** CURSOR: " + repr(cursor)
                print "****** COUNT: " + repr(count)
        except tweepy.error.TweepError:
            print count

if __name__ == "__main__":
    u = UserTest()
    u.dowloandFollowers()
    #print u.api.rate_limit_status()