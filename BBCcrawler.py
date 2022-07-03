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
    
    for item in newsItems:
        title = item.select_one("span.lx-stream-post__header-text.gs-u-align-middle").text
        
        try:
            
            image = item.select_one("img.qa-lazyload-image.lazyautosizes.lazyload")["data-src"]
            image = image.replace("{width}", "320")
        except: 
            print("2")
            continue

       
            
        
        
        article = {"title": title.strip(), "image" : image}
        print(title, image)
        results.append(article)
        
        print("1")
    
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
