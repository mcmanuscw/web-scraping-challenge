# Dependencies
from bs4 import BeautifulSoup
import pandas as pd 
import requests
import pymongo
import os
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
import time




def scrape():
    # Setup splinter
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Set an empty dict for listings that we can save to Mongo
    listings = {}

    #  URL to scrape Mars News
    url = 'https://redplanetscience.com/'
    
    # Call visit on our 0 and pass in the URL we want to scrape   
    browser.visit(url)

    # Let it sleep for 5 seconds
    time.sleep(5)

    # Fetch title using find x path... 
    news_title=browser.find_by_xpath('//*[@id="news"]/div[1]/div/div[2]/div/div[2]').text

    # Fetch teaser paragraph using find x path... 
    news_p=browser.find_by_xpath('//*[@id="news"]/div[1]/div/div[2]/div/div[3]').text

    #  URL to scrape featured image
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    time.sleep(5)


    # Fetch featured image... 
    # Copied xpath for clickable image - /html/body/div[1]/div/a/button
    browser.find_by_xpath('/html/body/div[1]/div/a/button').click()
    
    # xpath for  - /html/body/div[8]/div/div/div/div/img -->> right click on the image and inspect >> right click >> copy >> Copy xpath

    url_featured_image=browser.find_by_xpath('/html/body/div[8]/div/div/div/div/img')['src']
    
    #  URL to scrape Mars Facts
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)
    time.sleep(5)

    # Pandas to read the table and write the table to text html 
    table_df=pd.read_html(url)[0]
    table_df.columns=['Description', 'Mars', 'Earth']   
    table_df.set_index('Description', inplace=True)

    
    table_html=table_df.to_html()
    

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(5)

    hemisphere_image_urls = []

    # (1,5) 1 signifies for the loop to start in the second position
    # (1,5) 5 signifies for the loop to run 

    for i in range(1,5):
        xpath=f'//*[@id="product-section"]/div[2]/div[{i}]/div/a/h3'
        browser.find_by_xpath(xpath).click()
        
        
        url=browser.find_by_xpath('//*[@id="wide-image"]/div/ul/li[1]/a')['href']
        
        title=browser.find_by_xpath('//*[@id="results"]/div[1]/div/div[3]/h2').text
        hemis={}

        hemis["img_url"]=url
        hemis["title"]=title

        hemisphere_image_urls.append(hemis)
        browser.back()
    

    data = {
            "news_title": news_title,
            "news_paragraph": news_p,
            "featured_image": url_featured_image,
            "facts": table_html,
            "hemispheres": hemisphere_image_urls,
            "last_modified": dt.datetime.now()
        }




    # Quit the browser
    browser.quit()

    # Return our dictionary
    return data
