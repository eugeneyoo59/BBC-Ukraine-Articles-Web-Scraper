import requests
from bs4 import BeautifulSoup


headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}


def makeRequest():
    for i in range(0, 9):
        BBCrequest = requests.get("https://www.bbc.com/news/world-60525350", headers = headers)

        if BBCrequest.status_code != 200:
            print("Bad Request")
        else:
            return BBCrequest.text
        
BBCtext = makeRequest()
#print(BBCtext)
soup = BeautifulSoup(BBCtext, "html.parser")

results = []

def parseHTML():
    newsItems = soup.select(".gs-u-m0.gs-u-p0.lx-stream__feed.qa-stream > .lx-stream__post-container")
    counter =0
    for item in newsItems:
        if counter == 10:
            break
        counter = counter+1
        title = item.select_one("span.lx-stream-post__header-text.gs-u-align-middle").text
        print("_______")
        #print(title)
    
        try:
            #print("tried")
            #print(item)
            image = item.select_one(".qa-lazyload-image.lazyload")["data-src"]
            image = image.replace("{width}", "320")
            #print(image)
        except: 
            print("")

        try: 
            image = item.select_one(".qa-srcset-image.lx-stream-related-story--index-image.qa-story-image")["src"]
        except: 
            #print("line 43")
            counter = counter-1
            continue
       
            
        
        
        article = {"title": title.strip(), "image" : image}
        print(title, image)
        results.append(article)
        
        #print("1")
    
parseHTML()

print (results)


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "goormtest_web_apr.settings")
import django
django.setup()

from hello.models import Article

Article.objects.filter(source="BBC").delete()

for result in results:
    Article.objects.create(title=result["title"], image=result["image"], source="BBC")
 

#print(Article.objects.all())
