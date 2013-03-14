import random
from scrapy import log
from scrapy.utils.misc import load_object

from scrapy.core.scheduler import Scheduler

from Queue import PriorityQueue

import pdb

class BfsScheduler(Scheduler):

    def __init__(self, dupefilter, stats=None):
        self.df = dupefilter
        self.stats = stats
        self.requests = PriorityQueue()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        dupefilter_cls = load_object(settings['DUPEFILTER_CLASS'])
        dupefilter = dupefilter_cls.from_settings(settings)
        return cls(dupefilter, stats=crawler.stats)

    def has_pending_requests(self):
        return not self.requests.empty()

    def open(self, spider):
        self.spider = spider
        if self.requests:
            del self.requests
        self.requests = PriorityQueue()

    def close(self, reason):
        del self.requests
        return self.df.close(reason)

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            return
        self.requests.put((request.meta['potential_score'], request))
        self.stats.inc_value('scheduler/enqueued', spider=self.spider)

    def next_request(self):
        if not self.requests or not self.has_pending_requests():
            return
        request = self.requests.get_nowait()[1]
        log.msg("Next request to process with score %.2f: %s"%(request.meta['potential_score'], request.url))
        if request:
            self.stats.inc_value('scheduler/dequeued', spider=self.spider)
        return request
