#!/usr/bin/env python
# coding: utf-8

# In[15]:


# Dependencies
import os
import pandas as pd
import pprint
from IPython.display import display_html
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:

def scrape():
    data = {}

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[3]:


    url = 'https://redplanetscience.com'
    browser.visit(url)


    # In[4]:


    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # Retrieving first article object
    article_obj = soup.find('div', class_='content_title')

    article = article_obj.text
    
    data['headline'] = article


    # In[5]:


    # Navigating to next div from first article div ie. the text
    text = article_obj.findNext('div').text
    
    data['news'] = text


    # In[6]:


    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # In[7]:


    # Click on FULL IMAGE button
    browser.links.find_by_partial_text('FULL IMAGE').click()

    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # Getting image url
    featured_image_url = 'https://spaceimages-mars.com/' + soup.find('img', class_='fancybox-image')['src']
    
    data['featured'] = featured_image_url

    # In[8]:


    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)


    # In[9]:


    table = pd.read_html(url, flavor = 'html5lib')[0]
    
    data['table'] = table.to_html()

    # In[10]:


    url = 'https://marshemispheres.com'
    browser.visit(url)


    # In[11]:


    links = browser.links.find_by_partial_text('Hemisphere')
    hemisphere_image_urls = []

    #creating a dictionary for each link and storing in a list
    for link in links:
        d = {}
        d['title'] =  link.text
        d['img_url'] =  link['href'] #not the image url but the url for navigating
        hemisphere_image_urls.append(d)
        


    # In[12]:


    #go through each dictionary. navigate to url and overwriting with image url.
    for i in hemisphere_image_urls:
        
        browser.visit(i['img_url'])
        i['img_url'] = browser.links.find_by_partial_text('Original')['href']
        i['tmb_url'] = browser.links.find_by_partial_text('Sample')['href']

        


    # In[19]:

    data['hiu'] = hemisphere_image_urls

    # Quit the browser
    browser.quit()

    return data

