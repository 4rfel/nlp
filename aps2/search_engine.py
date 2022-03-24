import pymongo, certifi

class SearchEngine:
    def __init__(self, min_distance=100):
        self.min_distance = min_distance
        # pegar um certificado para conseguir acessar o banco de dados
        ca = certifi.where()
        # criando conexao com o banco de dados
        client = pymongo.MongoClient("mongodb+srv://nlp:nlphuehue@manga.9pvhp.mongodb.net/manga?retryWrites=true&w=majority", tlsCAFile=ca)

        self.db = client.nlp.keywords

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
        query = query.lower()
        result = self.db.find_one({"keyword":query})
        if result != None:
            # if the keyword is in the dataset, then return the list of titles that contain that keyword
            return result["keyword"][1]
        else:
            # if the keyword is not in the dataset, then change the query to the nearest keyword
            # using Levenshtein distance and return the list of titles that contain that keyword

            min_distance = self.min_distance
            keywords = self.db.find({}, {"_id": 0, "keyword": 1})
            nearest_keyword = ""
            for keyword in keywords:
                keyword = keyword["keyword"]
                distance = self.levenshtein_distance(query, keyword)
                if (distance < min_distance):
                    min_distance = distance
                    nearest_keyword = keyword


            result = self.db.find_one({"keyword":nearest_keyword})
            return result["keyword"][1]