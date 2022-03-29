import pymongo, certifi

class SearchEngine:
    def __init__(self, min_distance=100):
        self.min_distance = min_distance
        # pegar um certificado para conseguir acessar o banco de dados
        ca = certifi.where()
        # criando conexao com o banco de dados
        client = pymongo.MongoClient("mongodb+srv://nlp:nlphuehue@manga.9pvhp.mongodb.net/manga?retryWrites=true&w=majority", tlsCAFile=ca)

        self.db = client.nlp.keywords
        k = self.db.find({}, {"_id": 0, "keyword": 1})
        self.keywords = [x for x in k]

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

    def get_max_results(self, result, max_results):
        mangas = []
        current_results = 0
        for item in result["keyword"][1]:
            if current_results < max_results:
                mangas.append(item)
                current_results += 1
            else:
                break
        
        return mangas

    def search(self, query, max_results=10):
        query = query.lower()
        result = self.db.find_one({"keyword":query})
        if result != None:
            # if the keyword is in the dataset, then return the list of titles that contain that keyword
            # get only top 10 results
            mangas = self.get_max_results(result, max_results)
            return mangas, None
        else:
            # if the keyword is not in the dataset, then change the query to the nearest keyword
            # using Levenshtein distance and return the list of titles that contain that keyword

            min_distance = self.min_distance
            nearest_keyword = ""
            for keyword in self.keywords:
                keyword = keyword["keyword"][0]
                distance = self.levenshtein_distance(query, keyword)
                if (distance < min_distance):
                    min_distance = distance
                    nearest_keyword = keyword
                    
            result = self.db.find_one({"keyword":nearest_keyword})
            # get only top 10 results
            mangas = self.get_max_results(result, max_results)
                
            return mangas, f"voce digitou {query}, procurando por {nearest_keyword}"