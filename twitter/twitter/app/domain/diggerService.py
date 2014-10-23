
from twitter.app.domain.tasks import startDigger

class DiggerService:
    
    def startDiggerNow(self, _key):
        startDigger.delay(key=_key)
        
    def startDiggerLater(self, _key, date):
        startDigger.apply_async(key=_key, eta=date)
        