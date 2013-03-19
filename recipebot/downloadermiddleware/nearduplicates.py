from scrapy.stats import stats
from ndd.ndindex import NearDuplicatesIndex
from scrapy.exceptions import IgnoreRequest

class NearDuplicatesDetection(object):

    def __init__(self):
        self.index = NearDuplicatesIndex()

    def process_response(self, request, response, spider):
        doc = request.meta['terms']
        if self.index.appendif(doc, response.url, 0.0):
            return response

        stats.inc_value('downloader/near_duplicates')

        raise IgnoreRequest
