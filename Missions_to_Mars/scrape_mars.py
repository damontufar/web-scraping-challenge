
#Dependencies

from typing import Sequence
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    #Set up Splinter
    executable_path = {'executable_path' : ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = False)

    #MARS NEWS 
    url = 'https://redplanetscience.com/'
    browser.visit(url) 

    html = browser.html
    soup = bs(html, 'html.parser')

    #Collect the latest News Title and Paragraph Text
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    #MARS IMAGE

    #URL of the Space Image page to be scrapped
    url = 'https://spaceimages-mars.com/'   
    browser.visit(url)

    #Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = bs(html, 'html.parser')

    #Collect Image Source
    image_source = soup.find('img', class_='headerimage fade-in')
    featured_image_url = url+image_source['src']

    #MARS FACTS

    #URL of facts
    url = 'https://galaxyfacts-mars.com/'

    mars_table = pd.read_html(url)  
    
    #Select Mars facts table
    mars_df = mars_table[1]

    #Assign Columns Name
    mars_df.columns = ['Metric', 'Value']

    #Convert the data to a HTML table string.
    mars_html = mars_df.to_html()

    #MARS HEMISPHERES IMAGES 

    #URL of the Space Image page to be scrapped
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    #Obtain url for each hemisphere page

    hrefs = []
    item = soup.find_all('div', class_='item')

    for content in item:
        a = content.find('a')
        href = a['href']
        hrefs.append(url + href)


        #Loop trough each hemisphere page in order to obtain image url

    hemisphere_image_urls = []

    for link in hrefs:
        url = 'https://marshemispheres.com/'
        urls = link
        browser.visit(urls)
        html = browser.html
        soup = bs(html, 'html.parser')
        title = soup.find('h2', class_='title').text
        wide_image = soup.find('img', class_='wide-image')
        img = wide_image['src']
        img_url = url+img
        #Append Results
        data = {'title': title, 'img_url': img_url}
        hemisphere_image_urls.append(data)
       
    #Store data in a dictionary
    mars_dict = {
        "title" : news_title,
        "paragraph" : news_p,
        "image_url" : featured_image_url,
        "facts_table": mars_html,
        "hemisphere_images": hemisphere_image_urls
        }

    #Quit the browser
    browser.quit()

    #Return results
    return mars_dict