import scrapy
import time



class Link(scrapy.Item):
    link = scrapy.Field()

class movieLinks(scrapy.Spider):
    name = 'links_spider'
    allowed_domains = ['https://www.imdb.com/']
    try:
        with open("link_to_ranking.csv", "rt") as file:
            start_urls = [str(file.readlines()[1])]
    except:
        start_urls = []

    def parse(self, response):
        xpath = '//tbody[@class = "lister-list"]/tr/td[@class = "titleColumn"]/a/@href'
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            l['link'] = 'https://www.imdb.com/' + s.get()
            yield l
    
