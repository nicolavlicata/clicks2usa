import re
from simpleURL import *
from bs4 import BeautifulSoup

def distance(start):
    count = 0
    destination = '/wiki/United_States'
    visited = []
    visited2 = []
    queue = []
    html = simple_get(start)
    bsObj = BeautifulSoup(html, 'html.parser')
    queue.append({'url' : title2url(bsObj.title.string),   'prev': None})
    visited.append({'url' : title2url(bsObj.title.string), 'prev': None})
    visited2.append(title2url(bsObj.title.string))

    while queue:
        curr = queue.pop(0)
        #print(curr, end = '\n')

        if hasDest(curr['url'], destination):
            print("Found it!")
            return createPath(curr)

        for i in distanceHelp(curr['url']):
            if i not in visited2:
                queue.append({'url' : i, 'prev' : curr})
                visited.append({'url' : i, 'prev' : curr})
                visited2.append(i)

def createPath(page):
    path = []
    curr = page
    while curr != None:
        path.append(curr['url'])
        curr = curr['prev']

    print(path)
    return path

    
                
                
def hasDest(start, dest):
    html = simple_get(start)
    bsObj = BeautifulSoup(html, 'html.parser')
    for link in bsObj.find_all(href=re.compile('^/wiki/[a-zA-Z_]+$')):
        if link.get('href') == dest:
            return True

    return False
            
            
def title2url(title):
    url = 'https://en.wikipedia.org/wiki/'
    words = title.split()
    del words[len(words)-2:]
    for word in words:
        if word == words[len(words) - 1]:
            url += word
        else:
            url += word + '_'
    return url

def distanceHelp(url):
    mainPage = 'https://en.wikipedia.org/wiki/Main_Page'
    links = []
    html = simple_get(url)
    bsObj = BeautifulSoup(html, 'html.parser')
    for link in bsObj.find_all(href=re.compile('^/wiki/[a-zA-Z_]+$')):
        links.append('https://en.wikipedia.org' + link.get('href'))
    return list(filter(lambda k: mainPage not in k, links))
