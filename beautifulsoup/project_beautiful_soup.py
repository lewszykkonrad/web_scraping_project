from urllib import request
from bs4 import BeautifulSoup as BS
import re
import pandas as pd
import time

#method for measuring runtime
start = time.time()

# I am completing this project with assumption that we are starting on the home page of the domain, and direct ourselves
# to a subpage where the data we seek is located

#setting the limit boolean,, which if set to True will limit the nummber of scraped pages to 50
limit_boolean = True

#the homepage of IMDB
url = 'https://www.imdb.com/?ref_=nv_home'
html = request.urlopen(url)
bs = BS(html.read(), 'html.parser')

#here we obtain the link to the top 250 list of top rated movies on the website
# we iterate through options in the dropdown menu on the site until we find 'Top Rated Movie' that directs us to top 250 list
menu_items = bs.find_all('a', {'class' : 'ipc-list__item nav-link NavLink-sc-19k0khm-0 dvLykY ipc-list__item--indent-one'}, href = True)

for item in menu_items:
    if item.span.get_text() == 'Top Rated Movies':
        link = 'https://www.imdb.com/' + item['href']

#now we can access our top 250 list
html = request.urlopen(link)
bs = BS(html.read(), 'html.parser')

#now we will need to get the 250 links to each of the films in the ranking
film_list = bs.find_all('tbody', {'class' : 'lister-list'})[0].find_all('a')

#to make our operations easier, we will store the links in a list
links = []
for item in film_list:
    links.append('https://www.imdb.com/' + item['href'])

#each link gets scraped twice, but we need only one occurence. We omit every second element to avoid dupliactes
links = links[::2]
if limit_boolean:
    links = links[:100]

#we will collect the following information on each movie and store it in a dataframe
colnames = ['title', 'year', 'rating', 'budget', 'box_office', 'runtime', 'genre', 'director']
df = pd.DataFrame(columns = colnames)

#here we iterate through each movie url and scrape the information we need
for item in links:
    url = item
    html = request.urlopen(url)
    bs = BS(html.read(), 'html.parser')

    #title
    title = bs.find('div', {'class' : 'title_wrapper'}).find('h1').get_text()[:-8]

    #year of release
    year = bs.find('div', {'class' : 'title_wrapper'}).find('h1').get_text()[-6:-2]

    #user rating
    rating = bs.find('span', {'itemprop' : 'ratingValue'}).get_text()

    #budget
    try:
        budget = bs.find('h4', string = 'Budget:').nextSibling
        budget = re.findall('[1234567890,]', budget)
        budget = ''.join(budget).replace(',', '')
        budget = int(budget)
    except Exception:
        budget = None

    #worldwide box office
    try:
        box_office = bs.find('h4', string = 'Cumulative Worldwide Gross:').nextSibling
        box_office = re.findall('[1234567890,]', box_office)
        box_office = ''.join(box_office).replace(',', '')
        box_office = int(box_office)
    except Exception:
        box_office = None

    #runtime
    try:
        runtime = bs.find('h4', string = 'Runtime:').nextSibling.next.get_text()[:-4]
    except Exception:
        # for some of the movies, the runtime would not be specified in the technical section. An exception was needed,
        # where we have to convert the data from hour, minutes format to minutes
        runtime = bs.find('div', {'class':'title_wrapper'}).find('time').get_text()
        runtime = re.findall('\d+', runtime)
        runtime = str(int(runtime[0])*60 + int(runtime[1]))

    #genres
    genres = bs.find('h4', string = 'Genres:').parent.find_all('a')
    genres = [item.get_text() for item in genres]
    genres = ','.join(genres)

    #director
    try:
        director = bs.find('h4', string = 'Director:').next.next.next.get_text()
    except Exception:
        director = bs.find('h4', string = 'Directors:').parent.get_text().replace('  ', '').replace('\n', '').replace('Directors:', '')

    # We store the newly scraped data as a dictionary
    new_entry = {'title' : title, 'year' : year, 'rating' : rating,
                'budget' : budget, 'box_office' : box_office, 'runtime' : runtime, 'genre' : genres, 'director' : director}

    #and finally append it as a new row to our dataframe
    df = df.append(new_entry, ignore_index=True)
    
#saving our data to a csv file
df.to_csv('bs_data.csv', index=False, encoding= 'utf-8-sig')

# calulating total runtime
end = time.time()
final_time = end - start
print('runtime ---- ', final_time)