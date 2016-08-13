__author__ = 'erica'

from mole.app.utils import LoggerFactory
from apiclient.discovery import build

import json
import ast

import pymongo as p

logger = LoggerFactory.create_logger()

client = p.MongoClient()
db = client['mole']

CX_KEY = '013919317534392247185:rnabec_xu24'
API_KEY = 'AIzaSyBSI6xS_mfoj3iS9hTNOJR8lySimPTwE9o'
API_NAME = 'customsearch'
API_VERSION = 'v1'
DATE_RANGE = 'date:r:{date_from}:{date_to}'
HOST = 'https://news.google.com.ar'


class FilterService:

    def __init__(self):
        pass

    def generate_filters(self, keywords, date_from, date_to):
        logger.info("Starting generation of filters")
        query = ' '.join(keywords)
        date_range = DATE_RANGE.format(date_from=date_from.strftime("%Y%m%d"), date_to=date_to.strftime("%Y%m%d"))

        logger.info("Date range = " + date_range)

        service = build(API_NAME, API_VERSION, developerKey=API_KEY)
        response = service.cse().list(cx=CX_KEY, q=query, sort=date_range, googlehost=HOST).execute()
        response_json = ast.literal_eval(json.dumps(response, sort_keys=True))
        hashtags = []
        urls = []

        for item in response_json["items"]:
            urls.append(item["link"])

        logger.info("Generated: " + str(len(hashtags)) + " hashtags and " + str(len(urls)) + " urls")
        return {'hashtags': hashtags, 'urls': urls}