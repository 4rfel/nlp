import numpy as np

class SearchEngine:
    def __init__(self, inverted_keywords, min_distance=10):
        self.inverted_keywords = inverted_keywords
        self.min_distance = min_distance

    def levenshtein_distance_(self, s1, s2, n, max_depth):
        if n > max_depth:
            return -1
        if len(s1) == 0:
            return len(s2)
        if len(s2) == 0:
            return len(s1)
        if s1[0] == s2[0]:
            return self.levenshtein_distance_(s1[1:], s2[1:], n+1, max_depth)
        return 1 + min(self.levenshtein_distance_(s1, s2[1:], n+1, max_depth), self.levenshtein_distance_(s1[1:], s2, n+1, max_depth))

    def levenshtein_distance(self, s1, s2, max_depth=3):
        return self.levenshtein_distance_(s1, s2, 0, max_depth)

    def search(self, query):
        if (query in self.inverted_keywords):
            # if the keyword is in the inverted_keywords_list, then return the list of files that contain that keyword
            return self.inverted_keywords[query]
        else:
            # if the keyword is not in the self.inverted_keywords, then change the query to the nearest keyword
            # and return the list of files that contain that keyword using Levenshtein distance            

            min_distance = self.min_distance
            nearest_keyword = ""
            for keyword in self.inverted_keywords:
                distance = self.levenshtein_distance(query, keyword)
                if (distance < min_distance):
                    min_distance = distance
                    nearest_keyword = keyword

            return self.inverted_keywords[nearest_keyword]