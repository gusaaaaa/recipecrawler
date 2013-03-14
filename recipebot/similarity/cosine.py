import json
import math

def freq(term, doc):
    return doc.count(term)

def term_count(doc):
    return len(doc)

def tf(term, doc):
    return (freq(term, doc) / float(term_count(doc)))

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

def similarity(doc, index):
    if len(doc) == 0:
        return [0.0]
    v = {}
    for term in doc:
        v[term] = tf(term, doc)

    result = []
    for w in index:
        result.append(cosine(v, w))
    return result

class CosineSimilarity:
    def __init__(self, indexfile="index.json", threshold=0.7):
        content = ""
        with open(indexfile, "r") as f:
            content = f.read()
        self.index = json.loads(content)
        self.threshold = threshold

    def is_relevant(self, doc):
        return self.relevance(doc) > self.threshold

    def relevance(self, doc):
        result = similarity(doc, self.index)
        return max(result)
