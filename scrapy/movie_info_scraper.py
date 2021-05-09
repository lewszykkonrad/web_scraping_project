# -*- coding: utf-8 -*-
import scrapy
import re
import time


#setting up the page limit boolean
limt_boolean = True
if limt_boolean:
    limit = 101
else:
    limit = 251

class Movie(scrapy.Item):
    title       = scrapy.Field()
    release     = scrapy.Field()
    rating      = scrapy.Field()
    budget      = scrapy.Field()
    box_office  = scrapy.Field()
    runtime     = scrapy.Field()
    genre       = scrapy.Field()
    director    = scrapy.Field()

class InfoSpider(scrapy.Spider):
    name = 'movie_info_spider'
    allowed_domains = ['https: //www.imdb.com/']
    try:
        with open("movie_links.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:limit]
    except:
        start_urls = []
    
    def parse(self, response):
        m = Movie()

        title_xpath = '//div[@class = "title_wrapper"]/h1/text()'
        release_xpath = '//div[@class = "title_wrapper"]/h1/span[@id = "titleYear"]/a/text()'
        rating_xpath = '//div[@class = "ratingValue"]//span[@itemprop = "ratingValue"]/text()'
        budget_xpath = '//div[@class = "article" and @id = "titleDetails"]//div[@class = "txt-block"]/h4[@class = "inline" and text() = "Budget:"]/following-sibling::text()'
        box_office_xpath = '//div[@class = "article" and @id = "titleDetails"]//div[@class = "txt-block"]/h4[@class = "inline" and text() = "Cumulative Worldwide Gross:"]/following-sibling::text()'
        runtime_xpath = '//h4[@class = "inline" and text() = "Runtime:"]/following-sibling::time[1]/text()'
        genre_xpath = '//h4[@class = "inline" and text() = "Genres:"]/parent::div/a/text()'
        director_xpath = '//h4[@class = "inline" and text() = "Director:"]/following-sibling::a/text()'

        title = response.xpath(title_xpath).getall()[0]
        title = title.replace(u'\xa0', u' ')
        m['title'] = title

        m['release'] = response.xpath(release_xpath).getall()[0]
        m['rating'] = response.xpath(rating_xpath).getall()[0]

        try:
            budget = response.xpath(budget_xpath).getall()[0]
            budget = re.findall('[1234567890,]', budget)
            budget = ''.join(budget).replace(',', '')
            budget = int(budget)
            m['budget'] = budget
        except:
            m['budget'] = None

        try:
            box_office = response.xpath(box_office_xpath).getall()[0]
            box_office = re.findall('[1234567890,]', box_office)
            box_office = ''.join(box_office).replace(',', '')
            box_office = int(box_office)
            m['box_office'] = box_office
        except:
            m['box_office'] = None

        time = response.xpath(runtime_xpath).getall()[0]
        time = time[:-4]
        m['runtime'] = time

        genre = response.xpath(genre_xpath).getall()
        genre = ','.join(genre)
        m['genre'] = genre

        try:
            director = response.xpath(director_xpath).getall()[0]
        except:
            director_xpath = '//h4[@class = "inline" and text() = "Directors:"]/parent::div/a/text()'
            director = response.xpath(director_xpath).getall()
            director = ' '.join(director)
        
        m['director'] = director

        yield m

