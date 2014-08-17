from tweet_analizer.app.domain.authenticator import Authenticator
from tweet_analizer.app.domain.digger import Digger


class App:
    
    def run(self):
        a = Authenticator()
        d = Digger(a.authenticate())
        d.startStreaming()

#No funciona, tira error en el ConfigParser
if __name__ == "__main__":
    app = App()
    app.run()