# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "img_url_title": Mission_Mars(browser)
      
    }  

    #end scraping session
    browser.quit()
    return data

#separate functions
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page 
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #convert browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

      # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'


    return img_url

## Mars Facts
def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    # Assign columns and set index of dataframe    
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    return df.to_html(classes="table table-striped")

#mission to Mars
def Mission_Mars(browser):
     # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url) 
    html = browser.html
    
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    hrefs=[]
    img_title=[]
    jpg=[]
    
    
    try:
        # Parse HTML with Beautiful Soup
        hemi_soup = soup(html, 'html.parser')
    # Retrieve all elements that contain Hemisphere Info
        hemispheres = hemi_soup.find('div', class_='collapsible results')
    #hemispheres
        titles = hemispheres.find_all('h3')
        links = hemispheres.find_all('div', class_='item')
    
    #get titles                 
        for t in titles:
            title = t.text
            img_title.append(title)  
    #print (real_href) 
        for lin in links: 
            href= lin.find('a').get('href')
            real_href= f'https://marshemispheres.com/{href}'
            hrefs.append(real_href)
    
    #go to each link and get parent tag

        for ref in hrefs:
            browser.visit(ref)
            
            # Scrape from new links
            html = browser.html
            link_soup = soup(html, 'html.parser')
            jpg_link =link_soup.find('ul')
            jpg.append(jpg_link)
            #sleep(3)

    #get jpeg link

        for j in jpg:
            img_url=j.find('a').get('href')
            img_urlf=f'https://marshemispheres.com/{img_url}'
            hemisphere_image_urls.append(img_urlf)

    except BaseException:
        return None
#create dics
    lt=[dict(zip(["title"],[x])) for x in img_title]
    l=[dict(zip(["img_url"],[x])) for x in hemisphere_image_urls]
 # 4. Print the list that holds the dictionary of each image url and title.
    img_url_list=[]

    for x in range (0,4):
        l[x].update(lt[x])
        img_url_list.append(l[x])       

    return img_url_list

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())




    