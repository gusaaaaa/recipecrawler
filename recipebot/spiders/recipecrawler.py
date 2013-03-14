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

from recipebot.similarity import IntersectionLengthSimilarity, CosineSimilarity

import pdb

from urlparse import urlparse
from posixpath import basename, dirname

terms = re.compile(r'\b[a-z-]+\b', flags=re.IGNORECASE)
tokenize = lambda text: terms.findall(text)

RELEVANCY_TSHOLD = 2

RECIPE_KEYWORDS = set(['recipe', 'ingredient', 'cook', 'fish', 'beef',
    'pork', 'menu', 'food', 'dish', 'diet', 'fruit', 'egg'
    'vegetarian', 'gluten', 'oister', 'mussel'])

# sim = IntersectionLengthSimilarity(RECIPE_KEYWORDS, RELEVANCY_TSHOLD)
sim = CosineSimilarity(indexfile=settings.INDEX_FILE, threshold=0.5)

class RecipecrawlerSpider(CrawlSpider):
    name = 'recipecrawler'

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
        request.meta['potential_score'] = sim.relevance(request.meta['link_text'])
        return request

    def parse_item(self, response):
        item = RecipebotItem()

        # clean body
        orig_body = response.body_as_unicode()
        body = remove_tags_with_content(orig_body, which_ones=('script', 'head'))
        body = remove_tags(remove_comments(body))
        doc = tokenize(body.lower())

        # decide if the page is interesting
        if not sim.is_relevant(doc):
            stats.inc_value('recipe/filtered_out') # probably not recipe page
            return

        if settings.OUTPUT_CRAWLED_PAGES:
            parse_object = urlparse(response.url)
            path = parse_object.netloc + "_" + parse_object.path.replace('/', '_') + ".html"
            with open("tmp/" + path, "wb") as f:
                f.write(response.body)

        item['url'] = response.url

        return item
