from scrapy.utils.misc import load_object
from scrapy.spider import BaseSpider
from recipebot import settings

class ConfigurableSpider(BaseSpider):
    _spidercls = load_object(settings.SPIDER_CLASS)

    name = 'configurable'

    def __init__(self, *a, **kwargs):
        self._spider = self._spidercls()
        super(ConfigurableSpider, self).__init__(*a, **kwargs)

    def log(self, *a, **kwargs):
        self._spider.log(self, *a, **kwargs)

    def set_crawler(self, *a, **kwargs):
        self._spider.set_crawler(*a, **kwargs)

    @property
    def crawler(self):
        return self._spider.crawler

    @property
    def settings(self):
        return self._spider.settings

    def start_requests(self):
        return self._spider.start_requests()

    def make_requests_from_url(self, url):
        return self._spider.make_requests_from_url(url)

    def parse(self, response):
        return self._spider.parse(response)

    @classmethod
    def handles_request(cls, request):
        return cls._spidercls.handles_request(request)

    def __str__(self):
        return self._spider.__str__()

    __repr__ = __str__
