Manual:

BeautifulSoup - you just have to donwload the file and run the code. The code will output a csv file with all the data

Scrapy - There are three spiders. steps:
          1. First run the spider direct_to_ranking.py with command "scrapy crawl link_to_ranking_spider -o link_to_ranking.csv" /n
          2. Now run the spider movie_link_spider.py with command "scrapy crawl links_spider -o movie_links.csv"
          3. Lastly run the spider movie_info_scraper.py with command "scrapy crawl movie_info_spider -o movie_info.csv"
          4. Now you should have in total three csv file, movie_info.csv is the output with the movie data

Selenium - You have to update the geckodriver path in line 11, and just run the code. The code will output a csv file with data.

