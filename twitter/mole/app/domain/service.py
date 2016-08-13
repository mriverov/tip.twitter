from mole.app.domain.digger import Digger


# deprecado
class DiggerService:
    
    def __init__(self):
        pass

    def start_digger_now(self, keywords, project):
        Digger.start_digger(keywords, project)

