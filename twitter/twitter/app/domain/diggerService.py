from app.domain import tasks


class DiggerService:
    
    def __init__(self):
        pass

    @staticmethod
    def start_digger_now(domain, keyword, mention, hashtag):
        digger = tasks.start_digger(domain, keyword, mention, hashtag)
        tasks.start_streaming.delay(digger, keyword)
        tasks.start_streaming.delay(digger, mention)
        tasks.start_streaming.delay(digger, hashtag)

    @staticmethod
    def start_digger_later(_key, date):
        # tasks.start_digger.apply_async(_key, cursor=-1, eta=date)
        pass