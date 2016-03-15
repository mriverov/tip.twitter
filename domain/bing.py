import requests

from domain import LoggerFactory

BING_APP_ID = 'GR7QSZuKEfQaOWHqvzDW9ejA/GlB/Z9nBWwy5pAxKCQ'

BING_SEARCH_URL = 'https://api.datamarket.azure.com/Bing/Search/v1/News'


class BingProxy:


    def __init__(self):
        
        self.logger = LoggerFactory.create_logger()
    
    def search_in_bing(self,query):
        '''
        Searches in bing 
        
        '''
    
        params =  {
                   'Query':"'%s'" % (query) ,
                    '$format':'json',
                   }
    
    
        credentialBing = 'Basic ' + (':%s' % BING_APP_ID).encode('base64')[:]
        print credentialBing
        headers = {'content-type': 'application/json' ,
                    "Authorization":    credentialBing
                }
    
    
        self.logger.info("Searching bing for %s " % query)
        resp = requests.get(BING_SEARCH_URL, params=params,auth=("", BING_APP_ID),verify=False)
        if resp.status_code != 200:
            self.logger.warn( resp.text )
            return None
        else:
            respAsJson = resp.json()
            return respAsJson


if __name__ == '__main__':

    logger  = LoggerFactory.create_logger()

    bing = BingProxy()
    from py_bing_search import PyBingSearch
    
    s = "Anibal Fernandez Efedrina Lanata"
    
    #bing = PyBingSearch(BING_APP_ID)
    #result_list, next_uri = bing.search(s, limit=50, format='json')
    
    respAsJson = bing.search_in_bing(s)
    results = respAsJson['d']['results']
    for r in results:
        print r['Url']
