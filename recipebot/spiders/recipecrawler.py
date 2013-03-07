import re

from scrapy.stats import stats
from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from recipebot import settings
from recipebot.items import RecipebotItem

from w3lib.html import remove_tags_with_content, remove_tags, remove_comments

import pdb

from urlparse import urlparse

words = re.compile(r'\b[a-z-]+\b', flags=re.IGNORECASE)
tokenize = lambda text: words.findall(text)

RELEVANCY_TSHOLD = 2
RECIPE_KEYWORDS = set(['recipe', 'ingredient', 'cook', 'fish', 'beef',
    'pork', 'menu', 'food', 'dish', 'diet', 'fruit', 'egg'
    'vegetarian', 'gluten', 'oister', 'mussel'])

# intersection length should be greater than RELEVANCY_TSHOLD
is_relevant = lambda toks: len(RECIPE_KEYWORDS & set(toks)) > RELEVANCY_TSHOLD

ingredients_terms = re.compile(r'ingredients', re.IGNORECASE)
instructions_terms = re.compile(r'(directions|instructions|steps|method|preparation)', re.IGNORECASE)

def is_recipe(toks):
    has_ingredients = False
    has_instructions = False
    for t in toks:
        if has_ingredients and has_instructions:
            return True
        has_ingredients = ingredients_terms.match(t)
        has_instructions = instructions_terms.match(t)
    return False

def ingredient_line(tag):
    if not tag.string is None:
        if tag.find_parent(text = ingredients_terms):
            return True
    return False

class RecipecrawlerSpider(CrawlSpider):
    name = 'recipecrawler'

    start_urls = [ 'http://dmoz.org/' ]

    # TODO: extract only relevant links
    rules = (
            Rule(SgmlLinkExtractor(), callback='parse_item', follow=True),
            )

    def parse_item(self, response):
        item = RecipebotItem()

        # clean body
        orig_body = response.body_as_unicode()
        body = remove_tags_with_content(orig_body, which_ones=('script', 'head'))
        body = remove_tags(remove_comments(body))
        tokens = tokenize(body.lower())

        # decide if the page is interesting
        if not is_relevant(tokens):
            stats.inc_value('recipe/filtered_out') # probably not recipe page
            return

        parse_object = urlparse(response.url)
        path = parse_object.netloc + "_" + parse_object.path.replace('/', '_') + ".html"

        with open("tmp/" + path, "wb") as f:
            f.write(response.body)

        item['url'] = response.url

        return item
