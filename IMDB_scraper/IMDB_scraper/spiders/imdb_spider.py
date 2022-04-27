import scrapy

class ImdbSpider_Test(scrapy.Spider):
    name = "test"
    start_urls = ["https://www.imdb.com/name/nm0004266/"]
    
    def parse(self, response):
        actor = response.css('title').get()[7:].split(" - IMDb",1)[0]
        for movie_tv in response.css("div.filmo-row"):
            yield {
                "actor": actor,
                "movie_tv": movie_tv.css("a::text").get()
            }
          

          
          
class ImdbSpider(scrapy.Spider):
    name = "imdb_spider"
    start_urls = ["https://www.imdb.com/title/tt0816692/"]
    
    def parse(self, response):
        url = response.url + "fullcredits/"
        yield scrapy.Request(url, callback = self.parse_full_credit)
        
    def parse_full_credit(self, response):
        prefix = "https://www.imdb.com"
        suffixs = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        urls = [prefix + suffix for suffix in suffixs]
        for url in urls:
            yield scrapy.Request(url, callback = self.parse_actor_page)
        
    def parse_actor_page(self,response):
        actor = response.css('title').get()[7:].split(" - IMDb",1)[0]
        for movie_tv in response.css("div.filmo-row"):
            yield {
                "actor": actor,
                "movie_tv": movie_tv.css("a::text").get()
            }
          