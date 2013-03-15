from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from recipebot import settings

from scrapy.http import Request

class BfsSpider(CrawlSpider):

    def start_requests(self):
        requests = []
        f = open(settings.SEEDS_FILE)
        for url in f.readlines():
            request = Request(url.strip())
            request.meta['potential_score'] = 1.0
            requests.append(request)
        f.close
        return requests

    rules = (
            Rule(SgmlLinkExtractor(),
                 callback='parse_item',
                 process_request='set_score'),
            )

    def set_score(self, request):
        request.meta['potential_score'] = self.sim.relevance(request.meta['link_text'])
        return request
