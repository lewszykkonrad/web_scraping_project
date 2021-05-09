from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import pandas as pd


#here I set the limit boolean, which will limit the number of scraped pages to 50 if it is set to True
limit_boolean = True

gecko_path = 'C:/Users/lewsz/OneDrive/Desktop/UW_materials_semester_2/web_scraping/geckodriver'

url = 'https://www.imdb.com/'

options = webdriver.firefox.options.Options()
options.headless = False

driver = webdriver.Firefox(options = options, executable_path = gecko_path)

driver.get(url)
time.sleep(5)

#Here we access the link to the ranking, and set it as the new url
xpath = '/html/body/div[2]/nav/div[2]/aside/div/div[2]/div/div[1]/span/div/div/ul/a[3]'
item = driver.find_element_by_xpath(xpath)
href = item.get_attribute('href')
url = href

#now we can access the top 250 IMDB ranking
driver.get(url)
time.sleep(5)

#and here we scrape the 250 links to the movies in the ranking
xpath = '//tbody[@class = "lister-list"]/tr/td/a'
items = driver.find_elements_by_xpath(xpath)

#we create a list to store the links
list_of_links = []
for item in items:
    list_of_links.append(item.get_attribute('href'))

# each title link gets scraped twice, so we omit every second element
list_of_links = list_of_links[::2]
if limit_boolean:
    list_of_links = list_of_links[:100]

#We create an empty dataframe, where we willstore information on each of the movies
colnames = ['title', 'year', 'rating', 'budget', 'box_office', 'runtime', 'genre', 'director']
df = pd.DataFrame(columns = colnames)

# now we iterate through each title, and scrape the movie characteristics
for link in list_of_links:

    url = link
    driver.get(url)
    
    #title
    xpath = '//div[@class = "title_wrapper"]/h1'
    item = driver.find_element_by_xpath(xpath)
    title = item.text[:-6]
    
    #release year
    release = item.text[-5:-1]

    #rating
    xpath = '//div[@class = "ratingValue"]//span[@itemprop = "ratingValue"]'
    item = driver.find_element_by_xpath(xpath)
    rating = item.text

    #budget
    try:
        xpath = '//h4[@class = "inline" and text() = "Budget:"]'
        item = driver.find_element_by_xpath(xpath)
        item = item.find_element_by_xpath('..')
        budget = item.text
        budget = re.findall('[1234567890,]', budget)
        budget = ''.join(budget).replace(',', '')
        budget = int(budget)
    except:
            budget = None
            

    #box office
    try:
        xpath = '//div[@class = "article" and @id = "titleDetails"]//div[@class = "txt-block"]/h4[@class = "inline" and text() = "Cumulative Worldwide Gross:"]'
        item = driver.find_element_by_xpath(xpath)
        item = item.find_element_by_xpath('..')
        box_office = item.text
        box_office = re.findall('[1234567890,]', box_office)
        box_office = ''.join(box_office).replace(',', '')
        box_office = int(box_office)   
    except:
        box_office = None

    #runtime
    xpath = '//h4[@class = "inline" and text() = "Runtime:"]/following-sibling::time'
    item = driver.find_element_by_xpath(xpath)
    runtime = item.text
    runtime = runtime[:-4]

    #genre
    xpath = '//h4[@class = "inline" and text() = "Genres:"]'
    item = driver.find_element_by_xpath(xpath)
    item = item.find_element_by_xpath('..')
    genre = item.text
    genre = genre[8:]
    genre = genre.replace(' |', ',')

    #director
    try:
        xpath = '//h4[@class = "inline" and text() = "Director:"]'
        item = driver.find_element_by_xpath(xpath)
        item = item.find_element_by_xpath('../a')
        director = item.text

    except:
        xpath = '//h4[@class = "inline" and text() = "Directors:"]'
        item = driver.find_element_by_xpath(xpath)
        item = item.find_elements_by_xpath('../a')
        # item = item.find_elements_by_xpath('a')
        directors = []
        for director in item:
            directors.append(director.text)
        director = ', '.join(directors)

    # we organize the newly scraped data into a dictionary
    new_entry = {'title' : title, 'year' : release, 'rating' : rating,
                'budget' : budget, 'box_office' : box_office, 'runtime' : runtime, 'genre' : genre, 'director' : director}

    # and now we can append the data as a new row to our dataframe
    df = df.append(new_entry, ignore_index=True)

#finally
df.to_csv('selenium.csv', index=False, encoding= 'utf-8-sig')
driver.quit()
