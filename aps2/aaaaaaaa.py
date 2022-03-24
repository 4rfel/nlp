import pymongo, certifi, scrapy

# help(pymongo.MongoClient)

# pegar um certificado para conseguir acessar o banco de dados
ca = certifi.where()
# criando conexao com o banco de dados
client = pymongo.MongoClient("mongodb+srv://nlp:nlphuehue@nlp.qvsvw.mongodb.net/manga?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.manga.manga

x = db.find({}, {"_id": 0, "url": 1})
# db.delete_many({})
print(x)
# for i in x:
#     print(i)
#     break
