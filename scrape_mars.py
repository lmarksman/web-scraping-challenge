from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Setup splinter


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    all_data = {}
    latest_news = mars_news(browser)

    all_data["news"] = latest_news[0]
    all_data["paragraph"] = latest_news[1]
    all_data["featured_image"] = featured_img(browser)
    all_data["facts"] = mars_facts(browser)
    all_data["hemispheres"] = hemispheres(browser)
    browser.quit()
    return all_data

def mars_news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve all elements that contain headline information
    titles = soup.find_all('div', class_='content_title')

    news_title = titles[0].get_text() #first position
    # Retrieve all elements that contain headline information
    paragraphs = soup.find_all('div', class_='article_teaser_body')

    news_p = paragraphs[0].get_text() #first position

    return news_title, news_p

def featured_img(browser):
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Click the Full Image button
    featured_img_url = ''

    # Click the button
    browser.links.find_by_partial_text("FULL IMAGE").click()

    # Read the new html
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    # Look for the image name
    space_image = img_soup.find('img', class_='fancybox-image').get('src')

    # combine the image with the site
    featured_img_url = url + space_image
    return featured_img_url

def mars_facts(browser):
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)[1] # found the table in the second element
    tables.columns=['description', 'data']
    tables.set_index('description', inplace=True)
    
    return tables.to_html()

def hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # get the links for the hemispheres
    links = browser.links.find_by_partial_text('Hemisphere Enhanced')

    # setup an empty list
    hemisphere_image_urls = []

    # loop through the links to move to the different pages
    for link in range(len(links)):
        # Read the new html
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        # click the link to move the hemisphere page
        browser.links.find_by_partial_text('Hemisphere Enhanced')[link].click()
        
        # Read the new html
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        #scrape title and image url
        title = soup.find('h2', class_='title')
        title_text = title.text
        img_url = soup.find('img', class_='wide-image').get('src')
        
        # create a dictionary out of the information
        hemi_dict = {
                    'title': title_text,
                    'img_url': url + img_url
        }
        
        # add the dictionary to the list
        hemisphere_image_urls.append(hemi_dict)
        
        # return to the previous page so we can continue to the next link
        browser.back()

    return hemisphere_image_urls
