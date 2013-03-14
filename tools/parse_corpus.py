import sys
import re
import math
from optparse import OptionParser
import time
from operator import itemgetter
import json
import csv

class Unbuffered:
   def __init__(self, stream):
        self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

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
    sys.stdout = Unbuffered(sys.stdout)

    parser = OptionParser()
    parser.add_option("-t", "--output-format", dest="format", default="json",
                      help="index format (default: json; options: json, csv)",
                      metavar="FORMAT")
    parser.add_option("-i", "--input", dest="input_file", default="corpus.txt",
                      help="input file (default: corpus.txt)",
                      metavar="INPUT")
    parser.add_option("-o", "--index-file", dest="index_file", default="index.json",
                      help="index file name to be generated (default: index.FORMAT)",
                      metavar="INDEX")
    parser.add_option("-s", "--seeds-file", dest="seeds_file", default="seeds.txt",
                      help="seeds file name to be generated (default: seeds.txt)",
                      metavar="SEEDS")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                      help="print line being parsed to stdout")

    (options, args) = parser.parse_args()

    if not (options.format in ['json', 'csv']):
        parser.error("allowed formats: json, csv")

    if options.verbose:
        print "Parsing corpus..."

    url = re.compile(r"^CURRENT URL (.+)$")
    terms = re.compile(r"\b[a-z-]+\b", flags=re.IGNORECASE)
    seeds = []
    corpus = []
    with open(options.input_file, "r") as f:
        odd = True
        n = 0
        for line in f.readlines():
            n = n + 1
            if options.verbose:
                print "%06d: %s..."%(n, line[0:40])
            if odd:
                odd = False
                seeds.append(url.match(line).group(1))
            else:
                odd = True
                corpus.append(terms.findall(line.lower()))

    if options.verbose:
        print "Done."

    # build index

    start_time = time.time()

    if options.verbose:
        print "Building index..."

    index = []
    i = 0
    if options.verbose:
        print "Number of documents: %d"%(len(corpus),)
    for doc in corpus:
        items = {}
        i = i + 1
        doc_time = time.time()
        if options.verbose:
            print "  - Generating index for document #%06d..."%(i,),
        for term in doc:
            items[term] = tfidf(term, doc, corpus)
        index.append(items)
        if options.verbose:
            print "Done in %.2f seconds (total: %.2f seconds)."%(time.time() - doc_time, time.time() - start_time)
    outputfile = "%s.%s"%(options.index_file.rsplit(".", 1)[0], options.format)

    if options.format == 'json':
        with open(outputfile, "wb") as f:
            f.write(json.dumps(index))
    else:
        with open(outputfile, "wb") as f:
            writer = csv.writer(f)
            i = 0
            for items in index:
                i = i + 1
                writer.writerows([i, term, value] for (term, value) in items.items())

    if options.verbose:
        print "Done. Index generated in %.2f seconds. Index file: %s"%(time.time() - start_time, outputfile)

    # output seeds.txt

    if options.verbose:
        print "Generating seeds file...",

    with open(options.seeds_file, "w") as f:
        for seed in seeds:
            f.write(seed)
            f.write("\n")

    if options.verbose:
        print "Done. Seeds file: %s"%(options.seeds_file,)

