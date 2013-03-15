# Scrapy settings for recipebot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'recipebot'

SPIDER_MODULES = ['recipebot.spiders']
NEWSPIDER_MODULE = 'recipebot.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'recipebot (+http://www.yourdomain.com)'
USER_AGENT = 'recipebot (university assignment)'

SCHEDULER = 'recipebot.bfsscheduler.BfsScheduler'

SPIDER_MIDDLEWARES = {
    'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': None,
}

DOWNLOADER_MIDDLEWARES = {
    'recipebot.middleware.DuplicateDetection': 600,
}

EXTENSIONS = {
    'scrapy.contrib.closespider.CloseSpider': 600,
}

CLOSESPIDER_PAGECOUNT = 5

OUTPUT_CRAWLED_PAGES = True

SEEDS_FILE = "input/seeds.txt"

INDEX_FILE = "input/index.json"
