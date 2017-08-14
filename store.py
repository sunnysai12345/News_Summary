import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from collections import Counter,OrderedDict
d=pd.read_csv("output.csv",encoding="latin1")
d.drop_duplicates(subset=["headlines"],inplace=True)
d.reset_index(drop=True,inplace=True)
#d.describe()
d["ctext"]=[0 for i in range(len(d["text"]))]
count=0
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
    }
for i,head in enumerate(d["headlines"]):
    print(i)
    if d["read_more"][i]:
        if len(d["read_more"][i].split("/"))>2:
            link=d["read_more"][i].split("/")[2]
            try:
                r=requests.get(d["read_more"][i],headers=headers)
            except:
                time.sleep(10)
            if i%300==0:
                #d.to_csv("complete"+str(i)+".csv", index=False)
                time.sleep(10)
            if link=="www.hindustantimes.com":
                #r=requests.get(d["read_more"][i])
                soup=BeautifulSoup(r.content,"lxml")
                try:
                    txt=soup.find("div",{"itemprop":"articlebody"}).getText()
                    count=count+1
                    d["ctext"][i]=txt
                except:pass
            elif link=="indiatoday.intoday.in":
                soup=BeautifulSoup(r.content,"lxml")
                soup.find("span",{"itemprop":"articleBody"})
                txt=""
                try:
                    for s in soup.find("span",{"itemprop":"articleBody"}).findAll("p")[:-3]:
                        txt=txt+s.getText()
                    count=count+1
                    d["ctext"][i]=txt
                except:pass
            elif link=="www.theguardian.com":
                soup=BeautifulSoup(r.content,"lxml")
                soup.find("div",{"itemprop":"articleBody"})
                txt=""
                try:
                    for s in soup.find("div",{"itemprop":"articleBody"}).findAll("p"):
                        txt=txt+s.getText()
                    count=count+1
                    d["ctext"][i]=txt
                except:pass
print(count)
d.to_csv("complete"+str(i)+".csv", index=False)
