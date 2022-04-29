import scrapy
          
class ImdbSpider(scrapy.Spider):
    name = "imdb_spider"
    start_urls = ["https://www.imdb.com/title/tt0816692/"] #Movie Interstellar
    
    def parse(self, response):
	```
	redirect the start url to the fullcredits site
	```
        url = response.url + "fullcredits/"
        yield scrapy.Request(url, callback = self.parse_full_credit)
        
    def parse_full_credit(self, response):
	```
	redirect the fullcredits site to the actor/actress sites
	```
        prefix = "https://www.imdb.com"
        suffixs = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        urls = [prefix + suffix for suffix in suffixs]
        for url in urls:
            yield scrapy.Request(url, callback = self.parse_actor_page)
        
    def parse_actor_page(self,response):
	```
	generate all the movies and tv shows the actor/actress plays
	```
        actor = response.css('title').get()[7:].split(" - IMDb",1)[0]
	#only look for the div.filmo-row with id like 'actor-...' or 'actress-...'
        for movie_tv in response.css('div.filmo-row[id^="act"]'):
            yield {
                "actor": actor,
                "movie_tv": movie_tv.css("a::text").get()
            }
          