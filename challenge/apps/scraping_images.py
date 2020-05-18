# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from flask import jsonify

#Method called after clicking each thumbnail to get the title and the img_url
def get_image_info(img_url):
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    #Open new browser to get the info
    browser_img = Browser('chrome', **executable_path)
    browser_img.visit(img_url)
    
    #Wait a second for the page to load
    browser_img.is_element_present_by_text('title', wait_time=1)
    #Initialize soup for the page
    img_soup = BeautifulSoup(browser_img.html, 'html.parser')

    try:
        #Find the title from the h2 tag
        h2_tag = img_soup.find('h2', {'class': 'title'})
        title = h2_tag.text
        #Grab the downloads div as that is where the URLs are stored
        div_downloads = img_soup.find('div', {'class': 'downloads'})
        downloads_ul = div_downloads.find("ul")
        #Get the lis within the ul
        downloads_li = downloads_ul.find("li")
        #Get the a within the li
        a_href = downloads_ul.find("a")    
        img_url = a_href['href']
    except AttributeError:
        return None, None
    
    #Go back to the previous page and continue to the next thumb  
    browser_img.quit()
    
    return (title, img_url)

#Scrape method responsible for obtaining titles and urls for all Mars hemispheres
def scrape_images():
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)

    # Visit the mars nasa news site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemispheres = []
    #User Splinter to get all the divs
    div_imgs = browser.find_by_tag('div')
    for div in div_imgs:
        #Focus on divs with the class item
        if div['class'] == 'item':
            #Get the a hrefs within that div
            a_hrefs = div.find_by_tag("a")
            #In this case there is only 1 a href
            a_href = a_hrefs[0]
            #Verify the class name of the a href
            if a_href['class'] == 'itemLink product-item':
                img_url = a_href['href']
                #Click the thumb for each Hemisphere
                (title, img_url) = get_image_info(img_url)
                hemisphere = {}
                hemisphere['title'] = title
                hemisphere['img_url'] = img_url
                hemispheres.append(hemisphere)
    browser.quit()

    return {'hemispheres':hemispheres}

if __name__ == "__main__":
    # If running as script, print scraped data
    res = scrape_images()
    print(res)