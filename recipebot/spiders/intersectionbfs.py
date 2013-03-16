import re

from scrapy.stats import stats
from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from recipebot import settings
from recipebot.items import RecipebotItem

from w3lib.html import remove_tags_with_content, remove_tags, remove_comments

from scrapy.http import Request

from recipebot.similarity import IntersectionLengthSimilarity

from recipebot.spiders.bfs import BfsSpider

terms = re.compile(r'\b[a-z-]+\b', flags=re.IGNORECASE)
tokenize = lambda text: terms.findall(text)

class IntersectionBfsSpider(BfsSpider):

    name = 'intersectionbfs'

    def __init__(self, *a, **kwargs):
        self.sim = IntersectionLengthSimilarity(keywords=settings.KEYWORD_SET, threshold=settings.RELEVANCY_THRESHOLD)
        super(IntersectionBfsSpider, self).__init__(*a, **kwargs)

    def parse_item(self, response):
        item = RecipebotItem()

        # clean body
        orig_body = response.body_as_unicode()
        body = remove_tags_with_content(orig_body, which_ones=('script', 'head'))
        body = remove_tags(remove_comments(body))
        doc = tokenize(body.lower())

        # decide if the page is interesting
        if not self.sim.is_relevant(doc):
            stats.inc_value('recipe/filtered_out') # probably not recipe page
            return

        item['url'] = response.url

        return item

