from googleapiclient.discovery import build


class GoogleSearch(object):
    def __init__(self, api_key, cse_id):
        self.service = build("customsearch", "v1", developerKey=api_key)
        self.cse_id = cse_id

    def search(self, search_term, **kwargs):
        # https://developers.google.com/resources/api-libraries/documentation/customsearch/v1/python/latest/customsearch_v1.cse.html
        return self.service.cse().list(q=search_term, cx=self.cse_id, **kwargs).execute()
