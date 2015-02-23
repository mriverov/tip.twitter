from app.domain import tasks


class DiggerService:
    
    def __init__(self):
        pass

    @staticmethod
    def start_digger_now(domain, keyword):
        tasks.start_digger.delay(domain, keyword)

    @staticmethod
    def start_digger_later(_key, date):
        # tasks.start_digger.apply_async(_key, cursor=-1, eta=date)
        pass