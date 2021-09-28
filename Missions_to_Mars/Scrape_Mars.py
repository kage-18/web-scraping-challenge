#!/usr/bin/env python
# coding: utf-8

# # Set Up for Splinter

from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    # # Mars News from NASA
    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    
    #Set an HTML object
    html = browser.html
    
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retrieve the latest element that contains news title and news_paragraph
    news_result_title = soup.find_all('div', class_='content_title')[0].text
    news_result_par = soup.find_all('div', class_='article_teaser_body')[0].text
    print(news_result_title)
    print(news_result_par)

    # # JPL Mars Space Featured Image
    space_image_url = 'https://spaceimages-mars.com/'
    browser.visit(space_image_url)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    
    #Set an HTML object
    html_space = browser.html
    
    # Parse HTML with Beautiful Soup
    soup2 = bs(html_space, 'html.parser')
    
    image_url = soup2.find('img',attrs={'class':'fancybox-image'})['src']
    
    #Website URL
    web_main_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    featured_image_url = web_main_url + image_url
    
    #print(featured_image_url)
    
    # # Mars Facts
    mars_fact_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(mars_fact_url)
    mars_fact_df = tables[1]
    # mars_fact_df

    mars_fact_df.columns = ['Description','Value']
    mars_fact_df.set_index('Description', inplace=True)
    # mars_fact_df
    
    #to html
    with open('mars_facts_df.html', 'w') as ft:
        mars_fact_df.to_html(ft)

    # # Mars Hemipheres
    url_hems = 'https://marshemispheres.com/'
    browser.visit(url_hems)

    #HTML object
    html_hems = browser.html

    # Parse with Beautiful Soup
    soup_hems = bs(html_hems, 'html.parser')

    # Retrieve items that contain mars hemispheres info
    item = soup_hems.find_all('div', class_='item')


    hems_list = []
    hems_main_url = 'https://marshemispheres.com/'

    for i in item:
        title = i.find('h3').text
        partial_img = i.find('a', class_='itemLink product-item')['href']
        browser.visit(hems_main_url + partial_img)
        partial_html = browser.html
        soup_par = bs(partial_html, 'html.parser')
        image_url = hems_main_url + soup_par.find('img', class_='wide-image')['src']
        hems_list.append({"title": title, "img_url": image_url})

    # hems_list

    mars_data={
        'Mars_title':news_result_title,
        'Mars_paragraph': news_result_par,
        'Mars_featured_image': featured_image_url,
        'Mars_fact': mars_fact_df.to_html(),
        'Mars_hemispheres': hems_list}
    browser.quit()
    return mars_data

mars_datas = scrape()

class Main:
    Mars_title = mars_datas['Mars_title'],
    Mars_paragraph =  mars_datas['Mars_paragraph'],
    Mars_featured_image =  mars_datas['Mars_featured_image'],
    Mars_fact =  mars_datas['Mars_fact'],
    Mars_hemisphere_1 =  mars_datas['Mars_hemispheres'][0]['img_url']
    Mars_hemisphere_2 =  mars_datas['Mars_hemispheres'][1]['img_url']
    Mars_hemisphere_3 =  mars_datas['Mars_hemispheres'][2]['img_url']
    Mars_hemisphere_4 =  mars_datas['Mars_hemispheres'][3]['img_url']
    Mars_hemisphere_title_1 =  mars_datas['Mars_hemispheres'][0]['title']
    Mars_hemisphere_title_2 =  mars_datas['Mars_hemispheres'][1]['title']
    Mars_hemisphere_title_3 =  mars_datas['Mars_hemispheres'][2]['title']
    Mars_hemisphere_title_4 =  mars_datas['Mars_hemispheres'][3]['title']

# Read the HTML file
HTML_File=open('./templates/index.html','r')
s = HTML_File.read().format(p=Main())
index = open('./templates/index.html','w')
index.write(s)
index.close()