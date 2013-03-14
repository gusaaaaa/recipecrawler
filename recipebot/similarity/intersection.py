class IntersectionLengthSimilarity:
    def __init__(self, keywords, threshold):
        self.is_relevant = lambda toks: len(keywords & set(toks)) > threshold

    def relevance(self, doc):
        return 1.0 if self.is_relevant(doc) else 0.0
