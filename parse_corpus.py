import re
import math
from optparse import OptionParser
from operator import itemgetter
import json
import csv

# Corpus file structure:
#
# CURRENT URL http://allrecipes.com
# Cheap, Fast, Healthy Dinners With
# CURRENT URL http://cookeatshare.c
# Ham Party Rolls 107 views 1/4 c. 

def freq(term, doc):
    return doc.count(term)

def term_count(doc):
    return len(doc)

def num_docs_containing(term, doc_list):
    count = 0
    for doc in doc_list:
        if freq(term, doc) > 0:
            count += 1
    return count

def tf(term, doc):
    return (freq(term, doc) / float(term_count(doc)))

def idf(term, doc_list):
    tf = float(num_docs_containing(term, doc_list))
    if tf == 0:
        return 0
    else:
        return math.log(len(doc_list) / tf)

def tfidf(term, doc, doc_list):
  return (tf(term, doc) * idf(term, doc_list))

def dot(v1, v2):
    # vector v is of the form v["term"] = value, where value is the
    # result of calculating tf-idf of "term" in the document list.
    terms = set(v1.keys() + v2.keys())
    result = 0
    for term in terms:
        a = v1[term] if v1.has_key(term) else 0
        b = v2[term] if v2.has_key(term) else 0
        result = result + a * b
    return result

def norm(v):
    values = v.values()
    result = 0
    for q in values:
        result = result + q*q
    return math.sqrt(result)

def cosine(v1, v2):
    return dot(v1, v2) / (norm(v1) * norm(v2))

def similarity(v, index):
    result = []
    for w in index:
        result.append(cosine(v, w))
    return result

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-t", "--output-format", dest="format", default="json",
                      help="index format (default: json; options: json, csv)",
                      metavar="FORMAT")

    (options, args) = parser.parse_args()

    if not (options.format in ['json', 'csv']):
        parser.error("allowed formats: json, csv")

    url = re.compile(r"^CURRENT URL (.+)$")
    terms = re.compile(r"\b[a-z-]+\b", flags=re.IGNORECASE)
    seeds = []
    corpus = []
    with open("corpus.txt", "r") as f:
        odd = True
        for line in f.readlines():
            if odd:
                odd = False
                seeds.append(url.match(line).group(1))
            else:
                odd = True
                corpus.append(terms.findall(line.lower()))

    # build index
    index = []
    for doc in corpus:
        items = {}
        for term in doc:
            items[term] = tfidf(term, doc, corpus)
        index.append(sorted(items.items(), key=itemgetter(1), reverse=True))

    outputfile = "index.%s"%(options.format,)

    if options.format == 'json':
        with open(outputfile, "wb") as f:
            f.write(json.dumps(index))
    else:
        with open(outputfile, "wb") as f:
            writer = csv.writer(f)
            i = 0
            for items in index:
                i = i + 1
                writer.writerows([i, term, value] for (term, value) in items)
