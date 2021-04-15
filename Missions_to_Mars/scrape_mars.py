
#Dependencies

from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    #Set up Splinter
    executable_path = {'executable_path' : ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = False)

    url = 'https://redplanetscience.com/'
    browser.visit(url) 

    html = browser.html
    soup = bs(html, 'html.parser')

    #Collect the latest News Title and Paragraph Text
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    #URL of the Space Image page to be scrapped
    url = 'https://spaceimages-mars.com/'   
    browser.visit(url)

    #Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = bs(html, 'html.parser')

    #Collect Image Source
    image_source = soup.find('img', class_='headerimage fade-in')
    featured_image_url = url+image_source['src']

    #Store data in a dictionary
    mars_dict = {
        "title" : news_title,
        "paragraph" : news_p,
        "image_url" : featured_image_url
    }

    #Quit the browser
    browser.quit()

    #Return results
    return mars_dict