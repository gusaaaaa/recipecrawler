import re
from ndd.ndindex import NearDuplicatesIndex
from w3lib.html import remove_tags_with_content, remove_tags, remove_comments

terms = re.compile(r'\b[a-z-]+\b', flags=re.IGNORECASE)
tokenize = lambda text: terms.findall(text)

class TermsExtractor(object):
    def process_response(self, request, response, spider):
        # clean body
        orig_body = response.body_as_unicode()
        body = remove_tags_with_content(orig_body, which_ones=('script', 'head'))
        body = remove_tags(remove_comments(body))
        terms = tokenize(body.lower())
        request.meta['terms'] = terms
        request.meta['body'] = body

        return response
