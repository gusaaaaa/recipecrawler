import re

from scrapy.stats import stats
from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from recipebot import settings
from recipebot.items import RecipebotItem

from w3lib.html import remove_tags_with_content, remove_tags, remove_comments

import BodyTextExtractor

import pdb

words = re.compile(r'\b[a-z-]+\b', flags=re.IGNORECASE)
tokenize = lambda text: words.findall(text)

tags_pattern = r'<\/?[a-z][a-z0-9]*\b[^>]*>'
tags = re.compile(tags_pattern, flags=re.IGNORECASE)
tags_grouping = re.compile(r'(%s)' % tags_pattern, flags=re.IGNORECASE)
split_tags_and_text = lambda text: tags_grouping.split(text)
is_tag = lambda text: tags.match(text)

RELEVANCY_TSHOLD = 2
RECIPE_KEYWORDS = set(['recipe', 'ingredient', 'cook', 'fish', 'beef',
    'pork', 'menu', 'food', 'dish', 'diet', 'fruit', 'egg'
    'vegetarian', 'gluten', 'oister', 'mussel'])

# intersection length should be greater than RELEVANCY_TSHOLD
is_relevant = lambda toks: len(RECIPE_KEYWORDS & set(toks)) > RELEVANCY_TSHOLD

class RecipecrawlerSpider(CrawlSpider):
    name = 'recipecrawler'
    start_urls = ['http://www.dmoz.org/Home/Cooking/Recipe_Collections/']

    rules = (
            Rule(SgmlLinkExtractor(), callback='parse_item', follow=True),
            )

    def parse_item(self, response):
        item = RecipebotItem()
        orig_body = response.body

        p = BodyTextExtractor.HtmlBodyTextExtractor()
        p.feed(orig_body)
        p.close()

        body = p.body_text().decode('utf-8', 'replace')

        tokens = tokenize(body.lower())

        # decide if the page is interesting
        if not is_relevant(tokens):
            stats.inc_value('recipe/filtered_out') # probably not recipe page
            return

        item['keywords'] = tokens
        item['content'] = body
        item['url'] = response.url
        return item
