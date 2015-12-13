__author__ = 'Marina'

import json
import requests


class DashboardService:

    def __init__(self):
        pass

    def post_info(self):
        #url = 'https://app.cyfe.com/api/push/55ff21ff014a09138215531560314'
        url = 'https://app.cyfe.com/api/push/55ff2f093b5003569232491560362'
        data = {"data": [{"Date": "20150920", "Tweets":  "342"}]}
        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}
        requests.post(url, data=data_json, headers=headers)



if __name__ == '__main__':
    processor = DashboardService()
    processor.post_info()