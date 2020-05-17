#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup
import requests
import os


# In[2]:


# URL of Python reddit
url = 'https://www.reddit.com/r/Python/'
url = 'https://www.reddit.com/r/ProgrammingHumor/'


# In[3]:


# Retrieve page with the requests module
html = requests.get(url)


# In[4]:


filepath = os.path.join("Programmer-Humor.html")
with open(filepath, encoding='utf-8') as file:
    html = file.read()


# In[5]:


# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(html, 'html.parser')


# In[6]:


# Find the number of subscribers
results = soup.find_all('span', class_='number')


# In[7]:


# Examine the results, then determine element that contains sought info
# results are returned as an iterable list
print(results)
for r in results:
    print(r.text)


# In[8]:


num_subscribers = soup.find("span", class_="subscribers").find('span', class_="number").text
num_subscribers


# In[9]:


results = soup.find_all('div', class_='top-matter')


# In[10]:


# Loop through returned results
for r in results:
    title = r.find('p', class_='title')
    title_text = title.a.text
    
    try:
        thread = r.find('li', class_='first')
        
        comments = thread.text.lstrip()
        
        comments_num = int(comments.split()[0])
        
        link = thread.a['href']
        # Access the thread with CSS selectors
        # print(title)
        # The number of comments made in the thread
        
        # Parse string, e.g. '47 comments' for possible numeric manipulation
        # Access the href attribute with bracket notation

        # Run if the thread has comments
        if (comments_num):
            print('\n-----------------\n')
            print(title_text)
            print('Comments:', comments_num)
            print(link)
    except AttributeError as e:
        print(e)


# In[ ]:




