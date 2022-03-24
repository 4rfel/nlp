# Aqui vai ficar o buscador de fato
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances
import numpy as np

class SearchEngine:
    def __init__(self):
        pass

    def indexar(self, corpora):
        self.vec = TfidfVectorizer()
        self.data = self.vec.fit_transform(corpora)
        self.info = [c[0:200] for c in corpora]
        return

    def ranquear(self, string_de_busca, n_max=10):
        query = self.vec.transform([string_de_busca])
        dists = cosine_distances(query, self.data)
        idx = np.argsort(dists)
        print(idx)
        ret = [ self.info[i] for i in idx[0,0:n_max] ]
        return ret



