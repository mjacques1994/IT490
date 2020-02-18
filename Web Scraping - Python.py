from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import ssl
import os

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def get_page_content(url):
    try:
        html_response_text = urlopen(url).read()
        page_content = html_response_text.decode('utf-8')
        return page_content
    except Exception as e:
        return None
    


def clean_title(title):
    invalid_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for c in invalid_characters:
        title=title.replace(c,'')
    return title

#if re.search(term, page_text, re.I):
    

def get_url(soup):
    links = soup.find_all('a')
    urls=[]
    for link in links:
        urls.append(link.get('href'))
    return urls

def is_url_valid(url):
    if url is None:
        return False
    if re.search('#', url):
        return False
    match=re.search('^/wiki/', url)
    if match:
        return True
    else:
        return False

def reformat_url(url):
    match=re.search('^/wiki/', url)
    if match:
        return "https://en.wikipedia.org"+url
    else:
        return url
    
def save(text, path):
    f = open(path, 'w', encoding = 'utf-8', errors = 'ignore')
    f.write(text)
    f.close()

f = open("crawled_url.txt","w")
count = 0
all_urls = []
page_content = ""
seed1 = 'https://en.wikipedia.org/wiki/Music'
seed2 = 'https://en.wikipedia.org/wiki/Rapping'

lst = [seed1,seed2]
for i in lst:
    page_content=get_page_content(i)

    lst1 = ['song','rap','genre','notes','art','chords','theory','history','pop', 'media', 'technology','rock']
    
    soup = BeautifulSoup(page_content, 'html.parser')
    page_text = soup.get_text()
    title = soup.title.string
    title=clean_title(title)

    temp_urls = get_url(soup)
    for tmp in temp_urls:
        if tmp not in all_urls:
            all_urls.append(tmp)

for x in all_urls:
    
    if not is_url_valid(x):
        continue
    
    x = reformat_url(x)
    page_content=get_page_content(i)
    lst1 = ['song','rap','genre','notes','art','chords','theory','history','pop', 'media', 'technology','rock']   
          
    soup = BeautifulSoup(page_content, 'html.parser')
    page_text = soup.get_text()
    title = soup.title.string
    title=clean_title(title)

    page_text = page_text.lower() #lowercases all text on wiki page

    for term in lst1:
        if term in page_text:
            f.write(str(count) + ': ' + x + '\n')
            count += 1
            break
    if count > 500:
        break
            
f.close()
'''
Report:
The topic that I chose to crawl through my web crawler was Music. The two seed websites that I started with are:
1. https://en.wikipedia.org/wiki/Music
2. https://en.wikipedia.org/wiki/Rapping
Within the topic of music, I selected 12 terms.
Those terms are 'song','rap','genre','notes','art','chords','theory','history','pop', 'media', 'technology',and 'rock'.
The crawler was implemented through python. The first step was to initiatlize and define the two seed websites. From there, I created a list for the 12 terms.
I then called the Beautiful Soup package and told it to look for the title. The line "page_text = page_text.lower()" was meant so that the terms are not case sensitive (as per the instructions).
Then the last for loop was to organize the links accordingly. The "if count > 500" was to make sure there were exactly 500 links pulled. 

'''

