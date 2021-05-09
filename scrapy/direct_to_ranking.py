import scrapy
import time


class Link(scrapy.Item):
    link = scrapy.Field()

class linkToRanking(scrapy.Spider):
    name = 'link_to_ranking_spider'
    allowed_domains = ['https://www.imdb.com/']
    start_urls = ['https://www.imdb.com/']

    def parse(self, response):
        xpath = '/html/body/div[2]/nav/div[2]/aside/div/div[2]/div/div[1]/span/div/div/ul/a[3]/@href'
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            l['link'] = 'https://www.imdb.com/' + s.get()
            yield l
    
