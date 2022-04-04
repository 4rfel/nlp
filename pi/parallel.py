from pathos.multiprocessing import cpu_count, Pool, ThreadPool
from functools import partial



def do(X, vec):
    global oi
    def oi(doc, X, vec):
        wordlist = []
        n_ngram = 5

        for word in vec.vocabulary_.keys(): # para cada palavra
            word_idx = vec.vocabulary_[word]
            if X[doc, word_idx] > 0:
                wordlist.append( (X[doc,word_idx], word) )
        wordlist = sorted(wordlist, reverse=True)
        return wordlist[0:n_ngram]

    with Pool(cpu_count()) as p:
        return p.map(partial(oi, X=X, vec=vec), list(range(X.shape[0])))