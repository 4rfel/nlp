from ast import keyword
import pymongo, certifi

ca = certifi.where()
# criando conexao com o banco de dados
client = pymongo.MongoClient("mongodb+srv://nlp:nlphuehue@manga.9pvhp.mongodb.net/manga?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.nlp
manga = db.manga # {"_id": id, "title": title, "summary": manga summary, "keywords": {keyword: tf, keyword: tf, keyword: tf}}
keywords = db.keywords # {"_id": id, "keyword": (keyword, [title + ": " + summary, title + ": " + summary, title + ": " + summary])}

def invert_list(dic):
    inverted_dic = {}
    # montando a lista invertida
    for word, value in dic.items():
        for item in value:
            tf = item[0]
            doc = item[1]
            if doc in inverted_dic:
                inverted_dic[doc].append((tf, word))
            else:
                inverted_dic[doc] = [(tf, word)]

    # ordenando de forma decrescente com base no tf
    inverted_dic = {key.lower(): sorted(value, reverse=True) for key, value in inverted_dic.items()}

    # criando o dicionario de keywords no formato desejado {"keyword": (word, [title, title, title])}"}
    inverted_dict = []
    for word, value in inverted_dic.items():
        titles = []
        for item in value:
            titles.append(item[1])
        inverted_dict.append({"keyword": (word, titles)})
    return inverted_dict

# pegando todos os dados do dataset porem apenas os titulos e as keywords
mangas_ = manga.find()

# criando um dicionario no formato {title: [(tf, keyword), (tf, keyword), (tf, keyword)]}"}
key = {}
for m in mangas_:
    mangas = []
    for word, tf in m["keywords"].items():
        mangas.append((tf, word))
    key[m["title"] + ": " + m["summary"]] = mangas


inverted_key = invert_list(key)
# print(inverted_key)
# resetando o database
keywords.delete_many({})
# colocando os dados no database
keywords.insert_many(inverted_key)
