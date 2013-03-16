from urlparse import urlparse

class OutputPagesSpiderMiddleware(object):
    def process_spider_input(self, response, spider):
        parse_object = urlparse(response.url)
        path = parse_object.netloc + "_" + parse_object.path.replace('/', '_') + ".html"
        with open("tmp/" + path, "wb") as f:
            f.write(response.body)
