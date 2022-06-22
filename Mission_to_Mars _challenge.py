#!/usr/bin/env python
# coding: utf-8

# In[137]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[138]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[78]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page 
browser.is_element_present_by_css('div.list_text', wait_time=1)


# we're searching for elements with a specific combination of tag (div) and attribute (list_text). As an example, ul.item_list would be found in HTML as <ul class="item_list">.
#  also waiting one second before searching for components. The optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.

# In[79]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[80]:


slide_elem.find('div', class_='content_title')


# In[81]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[82]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[83]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[84]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[85]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[86]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[87]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[88]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[89]:


df.to_html()


# In[90]:


#end scraping session
browser.quit()


# In[91]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[92]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[93]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[94]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[95]:


slide_elem.find('div', class_='content_title')


# In[96]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[97]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[98]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[99]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[100]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[101]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[102]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[103]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[104]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[105]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[401]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
html = browser.html
browser.visit(url)


# In[402]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# In[403]:


# 3. Write code to retrieve the image urls and titles for each hemisphere.

# Parse HTML with Beautiful Soup
hemi_soup = soup(html, 'html.parser')
# Retrieve all elements that contain Hemisphere Info
hemispheres = hemi_soup.find('div', class_='collapsible results')
#hemispheres
titles = hemispheres.find_all('h3')
links = hemispheres.find_all('div', class_='item')
#links[1]  

hrefs=[]
img_title=[]
jpg=[]
for lin in links: 
    href= lin.find('a').get('href')
    real_href= f'https://marshemispheres.com/{href}'
    hrefs.append(real_href)
    
    #print (real_href)        
for t in titles:
    title = t.text
    img_title.append(title)
    
#print(hrefs)    
#print(img_title)        

#go to link from list and get jpg 

for ref in hrefs:
    browser.visit(ref)
    
    # Scrape here
    html = browser.html
    link_soup = soup(html, 'html.parser')
    jpg_link =link_soup.find('ul')
    jpg.append(jpg_link)
    #sleep(3)
#print(jpg) 

for j in jpg:
    img_url=j.find('a').get('href')
    img_urlf=f'https://marshemispheres.com/{img_url}'
    hemisphere_image_urls.append(img_urlf)
hemisphere_image_urls


# In[428]:



#list of dictionary

l=[dict(zip(["img_url"],[x])) for x in hemisphere_image_urls]
print(l)


# In[429]:


lt=[dict(zip(["title:"],[x])) for x in img_title]
print(lt)


# In[431]:


# 4. Print the list that holds the dictionary of each image url and title.
img_url_list=[]

for x in range (0,4):
    l[x].update(lt[x])
    img_url_list.append(l[x])
img_url_list


# In[416]:


# 5. Quit the browser
browser.quit()


# In[ ]:





# In[ ]:




