from scrapy.stats import stats
from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from recipebot import settings
from recipebot.items import RecipebotItem

from recipebot.helpers.ingredientsdetector import IngredientsDetector
from recipebot.similarity import CosineSimilarity
from recipebot.spiders.bfs import BfsSpider

class AdhocSpider(BfsSpider):
    name = 'adhoc'

    def __init__(self, *a, **kwargs):
        self.sim = CosineSimilarity(indexfile=settings.INDEX_FILE, threshold=settings.RELEVANCY_THRESHOLD)
        self.detector = IngredientsDetector()
        super(AdhocSpider, self).__init__(*a, **kwargs)

    def parse_item(self, response):
        item = RecipebotItem()

        body = response.meta['body']

        result = self.detector.extract(body)

        if len(result) == 0:
            stats.inc_value('recipe/filtered_out') # probably not recipe page
            return

        item['url'] = response.url

        item['ingredients'] = []
        for item in result:
            if item[2] >= 0.25:
                item['ingredients'].append(item[0])

        return item

