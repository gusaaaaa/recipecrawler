class IntersectionLengthClassifier:
    def __init__(self, keywords, threshold):
        self.is_relevant = lambda toks: len(keywords & set(toks)) > threshold
