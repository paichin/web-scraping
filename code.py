# coding: utf-8
#author:bingrong
from bs4 import BeautifulSoup
import requests
import re
import csv
import random
from time import sleep
import codecs
import os
import pandas as pd
from tqdm import tnrange, tqdm_notebook
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
              'Referer':'http://bbs.51credit.com/'}

with open("url_list_csv_pufa.csv","a") as csvfile: 
    url_list_csv = csv.writer(csvfile)
    url_list_csv.writerow(["id","url","title","author","pbl_tme","reply_num","look_num"])

#get features: 1.serial number／2.link／3.title／4.author／5.published time／6.reply number／7.look up number
#50 links per page
counter=0

for i in range(1,1001):    
	sleep(0.5*random.uniform(1,2))
    print(i)
    url = 'http://bbs.51credit.com/forum-13-{}.html'.format(str(i))
    print(url)
    url_req=session.get(url,headers=headers)
    html_detail=BeautifulSoup(url_req.text,"html.parser")
    main_list=html_detail.select("tr > th > a")#to scrap titles and links, create a list first
    main_list=list(main_list)
    l=list()
    for ele in main_list:
        str_main_list=re.findall("<a\sclass=\"s\sxst\"([\s\S]*)",str(ele))
        if len(str_main_list)!=0:
            l.append(str_main_list)
    #print(len(l))
    select_user_name=html_detail.select("td.by > cite > a")#create list of author
    select_user_name=list(select_user_name)
    select_user_name=select_user_name[::2]
    user_name_list=list()
    for element in select_user_name:
    select_pbl_tme=list(select_pbl_tme)
    pbl_tme_list=list()
    for element in select_pbl_tme:
        fd_tme=re.findall("<span\stitle=\"(\S*)\">",str(element))
        if len(fd_tme)==0:
            fd_tme=re.findall("<span>(\S*)<\/span>",str(element))
        pbl_tme_list.append(fd_tme)
    select_num_lk=html_detail.select("td.num")#create list of look up time
    select_num_lk=list(select_num_lk)
    num_lk_list=list()
    if i==1:
        del(select_num_lk)[0]
        del(select_num_lk)[0]
        del(select_num_lk)[0]#pufa
    del(select_num_lk)[0]
    del(select_num_lk)[0]
    
    for element in select_num_lk:
        num_lk_list.append(re.findall("<em>(\S*)<\/em>",str(element)))
    select_num_rpl=html_detail.select("td.num > a")#create list of reply number
    select_num_rpl=list(select_num_rpl)
    num_rpl_list=list()
    if i==1:
        del(select_num_rpl)[0]
        del(select_num_rpl)[0]
        del(select_num_rpl)[0]
        del(select_num_rpl)[0]#pufa
    for element in select_num_rpl:
        num_rpl_list.append(re.findall("html\">([1-9]*)",str(element)))
    
    if i==1:#if it is the first page then delete elements below to remove ads
        del(user_name_list)[0]
        del(user_name_list)[0]
        del(user_name_list)[0]
        del(user_name_list)[0]#pufa
        del(pbl_tme_list)[0]
        del(pbl_tme_list)[0]
        del(pbl_tme_list)[0]
        del(pbl_tme_list)[0]#pufa
        #print(len(user_name_list))
        #print(len(pbl_tme_list))
        #print(len(num_lk_list))
    html_no=0
    
    for url_01 in l:#write informations into the file
        #print('write')
        url=re.findall("href=\"([\s\S]*html)\"",str(url_01[0]))
        ttle=re.findall("onclick=[\s\S]*>([\s\S]*)<\/a>",str(url_01[0]))[0]
        if len(url)!=0:
            counter=counter+1
            link_http="http://bbs.51credit.com/"+url[0]
            #with open("url_list_csv.csv","a") as csvfile:
            with codecs.open('url_list_csv_pufa.csv', 'a', 'utf_8_sig') as csvfile:
                url_list_csv = csv.writer(csvfile)
                url_list_csv.writerow([counter,link_http,ttle,user_name_list[html_no][0],pbl_tme_list[html_no][0],num_rpl_list[html_no][0],num_lk_list[html_no][0]])
        html_no=html_no+1


lst0 = pd.read_csv('pufa_15_17.csv', engine='c')
lst1=lst0.iloc[:,2]
lst1=list(lst1)

#lst0["threadno"] = lst0["url"].apply(lambda x: re.findall("^.+thread\-(\d+).+",x)[0])

#lst0_list = lst0["threadno"].tolist()
#lst0_list


#scraping of contents 
for nb in range(0,len(lst1)):
    while True:
        try:
            url=lst1[nb]
            url_id=re.findall('http:.*.html',str(url))
            url_id=url_id[0]
            #print("1")
            print(url_id)
            if len(url_id)>0:
                print("4")
                s=nb
                sleep(2*random.uniform(1,2))
                url_req = session.get(url, headers=headers)
                soup = BeautifulSoup(url_req.text, 'html.parser')
                d=soup.select("td.t_f")
                if (len(d)==0):
                    d=[" "]
                    flag=1
                else:
                    flag=0
                d1=d[0]
                len1=len(d)
                if (flag==0):
                    text_0=re.findall(".+\(\)\;(.+)$",d1.text, re.DOTALL)
                    if (len(text_0)==0):
                        text_0=[" "]
                else:
                    text_0=[" "]
                text0=text_0[0].replace("\r","").replace("\n","")
                text1=re.sub("(Screenshot_[0-9\-]+.+上传)","",text0)
                text2=re.sub("\([0-9\.]+ KB.+上传","",text1)
                text3=re.sub("(QQ图片[0-9]+\.+png)","",text2)
                text=re.sub("(超级截屏[0-9\_]+\.+png)","",text3)
                txt_file = open(str(url[31:38])+'.txt','w+',encoding='utf-8')
                txt_file.write("%s\n"%(url_id))
                txt_file.write("%s\n"%(str(text)))
                if len1>1:
                    for j in range(1,len1):
                        dj=soup.select("td.t_f")[j]
                        dj=re.sub("(\<blockquote\>[\s\S]+?\<\/blockquote\>)","",str(dj))
                        rep0=re.sub("(.+?\s发表于+.+[1-9\-]*:[1-9\-]*)","",re.sub("(<.+?>)","",str(dj))).replace("\r","").replace("\n","").replace("\xa0","")
                        rep1=re.sub("[0-9A-Z]*\.jpg[\s\S]*上传","",rep0)
                        rep=re.sub("(本帖最后由[\s\S]*编辑)","",rep1)
                        txt_file.write("%s\n"%(str(rep)))
                print(5)
                len_nxt=len(soup.select("div#ct > div > div > a.nxt"))
                while len_nxt>0:
                    sleep(0.2*random.uniform(1,2))
                    a=soup.select("div#ct > div > div > a.nxt")
                    lk='http://bbs.51credit.com/'+re.findall("href=\"(.+?)\"",str(a))[0]
                    url_req = session.get(lk, headers=headers)
                    soup = BeautifulSoup(url_req.text, 'html.parser')
                    d_nxt=soup.select("td.t_f")
                    len2=len(d_nxt)
                    if len2>1:
                        for i in range(1,len2):
                            di=soup.select("td.t_f")[i]
                            di=re.sub("(\<blockquote\>[\s\S]+?\<\/blockquote\>)","",str(di))
                            rep0=re.sub("(.+?\s发表于+.+[1-9\-]*:[1-9\-]*)","",re.sub("(<.+?>)","",str(di))).replace("\r","").replace("\n","").replace("\xa0","")
                            rep1=re.sub("[0-9A-Z]*\.jpg[\s\S]*上传","",rep0)
                            rep=re.sub("(本帖最后由[\s\S]*编辑)","",rep1)
                            txt_file.write("%s\n"%(str(rep)))
                    len_nxt=len(soup.select("div#ct > div > div > a.nxt"))
                txt_file.close()
        except:
            continue
        break

