__author__ = 'erica'

from mole.app.utils import LoggerFactory
from apiclient.discovery import build
import json,ast

import pymongo as p

logger = LoggerFactory.create_logger()

client = p.MongoClient()
db = client['mole']

CX_KEY = '013919317534392247185:rnabec_xu24'
API_KEY = 'AIzaSyBSI6xS_mfoj3iS9hTNOJR8lySimPTwE9o'
API_NAME = 'customsearch'
API_VERSION = 'v1'


class FilterService:

    def __init__(self):
        pass

    def generate_filters(self, keywords):
        query = ' '.join(keywords)
        service = build(API_NAME, API_VERSION, developerKey=API_KEY)
        response = service.cse().list(q=query, cx=CX_KEY).execute()
        response_json = ast.literal_eval(json.dumps(response, sort_keys=True))
        hashtags = []
        urls = []

        for item in response_json["items"]:
            urls.append(item["link"])

        return {'hashtags': hashtags, 'urls': urls}