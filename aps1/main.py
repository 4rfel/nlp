
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from crawler import WebCrawler

initial_url = "https://mangaclash.com/"

# Configurando o web crawler.
settings = Settings(values={"LOG_ENABLED": "True", "LOG_LEVEL": "WARNING", "DEPTH_LIMIT": "5"})
# Setando as configuracoes do crawler.
process = CrawlerProcess(settings=settings)
# Setando o crawler.
process.crawl(WebCrawler, initial_url)
# Iniciando o crawler.
process.start()
