from scrapy.stats import stats
from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from recipebot import settings
from recipebot.items import RecipebotItem

from scrapy.http import Request

from recipebot.similarity import IntersectionLengthSimilarity

from recipebot.spiders.bfs import BfsSpider

class IntersectionBfsSpider(BfsSpider):

    name = 'intersectionbfs'

    def __init__(self, *a, **kwargs):
        self.sim = IntersectionLengthSimilarity(keywords=settings.KEYWORD_SET, threshold=settings.RELEVANCY_THRESHOLD)
        super(IntersectionBfsSpider, self).__init__(*a, **kwargs)

    def parse_item(self, response):
        item = RecipebotItem()

        doc = response.meta['terms']

        # decide if the page is interesting
        if not self.sim.is_relevant(doc):
            stats.inc_value('recipe/filtered_out') # probably not recipe page
            return

        item['url'] = response.url

        return item

