import requests
from bs4 import BeautifulSoup 
import pandas as pd 
import time 
from multiprocessing import Process, Queue, Pool, Manager
from contextlib import closing
import threading
import sys


startTime = time.time()
qcount = 0 
products=[] 
prices=[] 
ratings=[] 
categories=[]
no_pages = 5 



def get_data(webPage, category, pageNo, q):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    r = requests.get(webPage+str(pageNo), headers=headers)
    content = r.content
    soup = BeautifulSoup(content, features="lxml")

    #print(soup)

    for d in soup.findAll('div', attrs={'class':'sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32'}):
        name = d.find('span', attrs={'class':'a-size-base-plus a-color-base a-text-normal'})
        price = d.find('span', attrs={'class':'a-offscreen'})
        rating = d.find('span', attrs={'class':'a-declarative'})
        all=[]
        if name is not None:
            all.append(name.text)
        else:
            all.append("unknown-product")
        if price is not None:
            all.append(price.text)
        else:
            all.append('varies')
        if rating is not None:
            all.append(rating.text)
        else:
            all.append('-1')
        all.append(category)
        q.put(all)

results = []

if __name__ == "__main__":
    m = Manager()
    q = m.Queue()
    webPages={"Horror": "https://www.amazon.com/s?k=horror+gifts&page=", "Drama":"https://www.amazon.com/s?k=drama+gifts&page=", "Comedy":"https://www.amazon.com/s?k=comedy+gifts&page=", "Action":"https://www.amazon.com/s?k=action+figures&page=", "Science Fiction": "https://www.amazon.com/s?k=sci+fi+gifts&page=", "Animation": "https://www.amazon.com/s?k=disney+gifts&page=", "Mystery":"https://www.amazon.com/s?k=gifts+for+mystery+fans&page=", "Adventure":"https://www.amazon.com/s?k=adventure+gifts&page=", "Documentary":"https://www.amazon.com/s?k=gifts+for+documentary+fans&page="}
    for webCat in webPages.keys():
        wp=webPages[webCat]
        pool_tuple = [(wp, webCat, x, q) for x in range(1,no_pages)]
        with Pool(processes=3) as pool:
            results = pool.starmap(get_data, pool_tuple)

while q.empty() is not True:
        qcount = qcount+1
        queue_top = q.get()
        products.append(queue_top[0])
        prices.append(queue_top[1])
        ratings.append(queue_top[2])
        categories.append(queue_top[3])


df = pd.DataFrame({'Product Name':products, 'Price':prices, 'Ratings':ratings, 'Category': categories})
df.to_csv('products.csv', index=False, encoding='utf-8')
