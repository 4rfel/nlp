from ast import keyword
import pymongo, certifi, scrapy, urllib

url_sw = "https://gist.github.com/alopes/5358189#file-stopwords-txt"
stopwords = urllib.request.urlopen(url_sw).read().decode().split()
stopwords = set(stopwords)

class WebCrawler(scrapy.Spider):
    def __init__(self, initial_url):
        self.start_urls = [initial_url]

        self.visited_urls = []
        # pegar um certificado para conseguir acessar o banco de dados
        ca = certifi.where()
        # criando conexao com o banco de dados

        client = pymongo.MongoClient("mongodb+srv://nlp:nlphuehue@manga.9pvhp.mongodb.net/manga?retryWrites=true&w=majority", tlsCAFile=ca)
        # client = pymongo.MongoClient("mongodb+srv://nlp:nlphuehue@nlp.qvsvw.mongodb.net/manga?retryWrites=true&w=majority", tlsCAFile=ca)
        self.db = client.nlp.manga
        # cleaning the database
        self.db.delete_many({})
    
    def parse(self, response):

        # Pegar o titulo da pagina.
        title = response.css("title::text").get().strip().replace("\n", "").replace("- MangaClash", "").replace("[New Chapters] Online Free", "").replace("Read", "").replace("English", "").replace("Manga", "").strip()

        # Checar se a pagina ainda n foi visitada para evitar loops
        if response.url not in self.visited_urls:
            # Colocar a pagina no banco de dados.

            # find "summary__content show-more" on response.body and get the next paragraph and remove all html tags in case summary is not None
            summary = response.css("div.summary__content.show-more").get()
            if summary is not None:
                summary = summary.replace("<p>", "").replace("</p>", "").replace("<br>", "").replace("</div>", "")
                summary = summary[summary.find(">")+1:]

                keys = summary.split(" ") + title.split(" ")
                
                # calculando tf e removendo stopwords
                keywords = {}
                for k in keys:
                    if k in stopwords:
                        continue
                    k = k.replace("\n", "").replace("\r", "").replace("\t", "").replace("\xa0", "").replace("!", "").replace("?", "")
                    if k not in keywords:
                        keywords[k] = 1
                    else:
                        keywords[k] += 1

                # mandando para o banco de dados
                self.db.insert_one({"title":title, "summary":summary, "keywords":keywords})

            # Adicionar a pagina visitada.
            self.visited_urls.append(response.url)
            print(f"Crawled {title}\t{response.url}")

        # Visitar os links da pagina.
        for link in response.css("a::attr(href)").getall():
            if link.startswith("http") or link.startswith("https"):
                yield response.follow(link, callback=self.parse)
