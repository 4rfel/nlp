import pymongo, certifi, scrapy

# pegar um certificado para conseguir acessar o banco de dados
ca = certifi.where()
# criando conexao com o banco de dados
client = pymongo.MongoClient("mongodb+srv://nlp:nlphuehue@nlp.qvsvw.mongodb.net/manga?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.manga.manga


class WebCrawler(scrapy.Spider):
    def __init__(self, initial_url):
        self.start_urls = [initial_url]

        self.visited_urls = []

    def parse(self, response):

        # Pegar o titulo da pagina.
        title = response.css("title::text").get().strip().replace("\n", "")

        # Checar se a pagina ainda n foi visitada para evitar loops
        if response.url not in self.visited_urls:
            # Colocar a pagina no banco de dados.
            db.insert_one({"url":response.url, "title":title, "content":response.body})

            # Adicionar a pagina visitada.
            self.visited_urls.append(response.url)
            print(f"Crawled {title}\t{response.url}")

        # Visitar os links da pagina.
        for link in response.css("a::attr(href)").getall():
            if link.startswith("http") or link.startswith("https"):
                yield response.follow(link, callback=self.parse)
