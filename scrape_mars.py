#Load Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup 
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url ='https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(5)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Save latest news title and paragraph snippet to variables
    news_date = soup.find_all("div",class_="list_date")[0].text
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find('div', class_='article_teaser_body').text
    #print(f'Date: {news_date}')
    #print(f'Title : {news_title}')
    #print (f'Snippet : {news_p}')

    ##Setup browser and Beautiful Soup for https://spaceimages-mars.com
    img_url = "https://spaceimages-mars.com"
    browser.visit(img_url)
    time.sleep(5)
    img_html = browser.html
    img_soup = soup(img_html,'html.parser')

    #use .find() to scrape source 
    image = img_soup.find("img", class_="headerimage fade-in")['src']
    featured_image_url = img_url + '/' +image

    #Pandas to scrape the table containing facts
    table_url = 'https://galaxyfacts-mars.com'
    table = pd.read_html(table_url)

    #Create dataframe 
    df = table[0]
    df.columns = df.iloc[0]
    df = df[1:]

    #Convert to html table string
    result = df.to_html(index=False)
    result = result.replace('\n','')

    #Set up for scrape of https://marshemispheres.com/
    hem_url = 'https://marshemispheres.com/'
    browser.visit(hem_url)
    time.sleep(5)
    # Create BeautifulSoup object; parse with 'html.parser'
    hem_html = browser.html
    hem_soup = soup(hem_html, 'html.parser')
    queries = hem_soup.find_all("div",class_ = "item")

    #create lists for dicts 
    titles = []
    img_urls = []
    #forloop to extract desired urls 
    for i in range(len(queries)):
        titles.append(queries[i].h3.text)
        img_urls.append("https://marshemispheres.com/" + queries[i].img["src"])
    
    hem_image_urls = []
    for title, img_url in zip(titles,img_urls):
        hem_image_url = {'title':title,'img_url':img_url}
        hem_image_urls.append(hem_image_url)

    print("Item in hem_image_urls : ")
    for index, item in enumerate(hem_image_urls):
        print(f"item{index} has values {item['title']} and {item['img_url']}")

    combined_dict = {'News title': news_title,
                     'News Snippet': news_p,
                     'Featured_image': featured_image_url,
                     'Mars_Earth_comparison': result, 
                     'Mars_Hemispheres': hem_image_urls}
    browser.quit()
    return combined_dict


