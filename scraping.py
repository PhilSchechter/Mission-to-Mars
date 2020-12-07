# import splinter and beautiful soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import datetime as dt
import re

# set executable path and initialize the chrome browser in splinter
executable_path = {'executable_path' : ChromeDriverManager().install()}
print(executable_path)
quit


def scrape_all():
    # intitiate headless driver for deployment
    #executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome',**executable_path,headless=True)
    news_title,news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "new_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere":mars_hemispheres(browser)
    }
    
    #stop webdriver and return data
    browser.quit()
    print('finishing scrape_all')
    return data

def mars_news(browser):
    # go to mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # optional delay for opening the page
    browser.is_element_present_by_css('ul.item_list li.slide',wait_time=1)

    html = browser.html
    news_soup = soup(html,'html.parser')
    slide_elem = news_soup.select_one('ul.item_list li.slide')
    # add try/excep for error handling
    try:
        slide_elem.find("div", class_='content_title')
        # use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None,None

    print('finishing browser')
    return news_title, news_p


### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # find and click the full_image button
    full_image_elem=browser.find_by_id('full_image')
    full_image_elem.click()

    # find and click the more_info button
    browser.is_element_present_by_text('more info',wait_time=1)
    more_info_elem=browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # parse the resulting html with soup
    html = browser.html
    img_soup=soup(html,'html.parser')

    
    try:
        #find the relative image url
        img_url_rel=img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return NotImplemented

    # use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    print('finishing image')
    return img_url


# mars facts
def mars_facts():
    try:
        # use read_html to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    df.columns=['description','value']
    df.set_index('description',inplace=True)
    return df.to_html()

def mars_hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # browser = Browser('chrome',**executable_path,headless=True)
    browser.visit(url)
    hemisphere_image_urls = []
    html = browser.html
    # optional delay for opening the page
    browser.is_element_present_by_css('container',wait_time=1)
    isoup=soup(html,'html.parser')
    
    # create links for hemisphere JPGs

    prefix = 'astropedia.astrogeology.usgs.gov'
    suffix = ".tif/full.jpg"

    # the search picks up each URL twice, so only keep every other instance
    links = []
    for link in isoup.find_all('a',class_='itemLink'):
        h_ref = link.get('href')
        img_url = f'https://{prefix}{h_ref}{suffix}'
        img_url = re.sub('search/map','download',img_url)
        #links.append([link.get('href')])
        links.append(img_url)
    links = [links[val] for val in [0,2,4,6]]

    # Create titles for image JPGs

    titles = []
    for stuff in isoup.find_all('h3'):
        title = stuff.get_text()
        img_url = f'{prefix}{title}{suffix}'
        titles.append(title)
        links.append(img_url)

    # 4. Return list that holds the dictionary of each image url and title.
    hemisphere_image_urls = []
    for i in range(4):
        entry = {"img_url":links[i], "title":titles[i]}
        hemisphere_image_urls.append(entry)
    return hemisphere_image_urls


if __name__ == "__main__":
    # if running as script, print scraped data
    print(scrape_all())
