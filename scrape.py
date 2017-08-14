import requests
from bs4 import BeautifulSoup
import pandas as pd

def storedata(soup):
    for data in soup.findAll("div",{"class":"news-card z-depth-1"}):
        #print(dict["headlines"],data.find(itemprop="headline").getText())
        if data.find(itemprop="headline").getText() not in dict["headlines"]:
            #print(data.find(itemprop="headline").getText(),dict["headlines"].index(data.find(itemprop="headline").getText()))
            dict["headlines"].append(data.find(itemprop="headline").getText())
            dict["text"].append(data.find(itemprop="articleBody").getText())
            dict["date"].append(data.find("span",{"clas":"date"}).getText())
            dict["author"].append(data.find("span",{"class":"author"}).getText())
            if data.find("a",{"class":"source"}):
                dict["read_more"].append(data.find("a",{"class":"source"}).get("href"))
            else:
                dict["read_more"].append("None")
    #print(len(dict["headlines"]))
url="https://www.inshorts.com/en/read"
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
    }
r=requests.get(url,headers=headers)
soup=BeautifulSoup(r.content,"lxml")
dict={"headlines":[],"text":[],"date":[],"author":[],"read_more":[]}
storedata(soup)
#Start Ajaxing
start_id=soup.findAll("script",{"type":"text/javascript"})[-1].getText().split()[3].strip(";").strip('"')
for i in range(1000000):
    print(i,len(dict["headlines"]))
    ajax_url="https://www.inshorts.com/en/ajax/more_news"
    payload={"news_offset":start_id}
    #print(payload)
    try:
        r=requests.post("https://www.inshorts.com/en/ajax/more_news",payload,headers=headers)
        soup=BeautifulSoup(r.text.replace('\\',""),"lxml")
        start_id=soup("p")[0].getText()[15:26].strip('"')
    #print(start_id)
        storedata(soup)
    except:
        pass
    if i%1000==0:
        df = pd.DataFrame(dict)
        df.to_csv("data"+str(i/1000)+".csv", index=False)
        dict = {"headlines": [], "text": [], "date": [], "author": [], "read_more": []}

