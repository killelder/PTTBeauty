# coding=UTF-8
import requests
import numpy
import time
import sys   
import os
import re
import urllib
#遞迴深度
sys.setrecursionlimit(1000000)
from bs4 import BeautifulSoup
class PTT:
    def __init__(self):
        self.board = []
        if os.path.exists("./boardinfo.txt"):
            boardinfo = open("./boardinfo.txt", "r")
        for buf in boardinfo:
            if not buf:
                break
            buf2 = buf.split(",")
            self.board.append(buf2[1].replace("\n",""))
"""class BBSboard:
    def __init__(self, cn, url):"""
#super compare with ptt board boardinfo.txt
def scpb(url, p):
    for boardurl in p.board:
        if sc(boardurl, url):
            return 0
    return 1
    
#super compare
def sc(f, s):
    for i in range(0, len(f)):
        if cmp(f[i:i+len(s)], s) == 0:
            return True
    return False

def req_loop(url, count):
    try:
        res = requests.get(url)
        return res
    except:
        if count > 10:
            return None
        else:
            res = req_loop(url, count + 1)
            return res
    
        
def getboardindex(url, thispage, gc):
    res = req_loop(url, 0)
    #res = ""
    #try:
    #    res = requests.get(url)
    #except:
    #    getboardindex(url, thispage, gc + 1)
    #print res
    soup = BeautifulSoup(res.text.encode("utf-8"))
    #print url
    soup2 = soup.findAll("div", id = "action-bar-container")
    boardend = 0
    if len(soup2) > 0:
        soup3 = soup2[0].findAll('a', href = True)
        #print url2
        for url2 in soup3:
            if sc(url2['href'], "bbs"):
                if len(re.findall("\d+", url2['href'])) > 0:
                    if int(re.findall("\d+", url2['href'])[0]) != 1:
                        if int(re.findall("\d+", url2['href'])[0]) < thispage or thispage == 0:
                            boardend = int(re.findall("\d+", url2['href'])[0])#print url2['href']
    return boardend
#從熱門 or 首頁
def ExtractBoard(url, boardinfo, p, count):
    res = requests.get(url)
    soup = BeautifulSoup(res.text.encode("utf-8"))
    time.sleep(0.1)
    #print url
    #super compare with ptt board
    if scpb(url, p) == 0:
        return 0
    #熱門看板特殊處理方式
    if sc(url, "https://www.ptt.cc/hotboard.html"):
        soup2 = soup.findAll("table")
    else:
        soup2 = soup.findAll("div", id = "prodlist")
    
    if len(soup2) == 0:
        soup2 = soup.findAll("title")
        if len(soup2) == 0:
            if count < 3:
                ExtractBoard(url, boardinfo, p, count + 1)
        else:     
            boardinfo.write(soup2[0].text.encode("utf-8"))
            boardinfo.write(",")
            boardinfo.write(url)    
            boardinfo.write("\n")
            ptt.board.append(url)
    else:
        for soup3 in soup2:
            url2 = soup3.findAll('a', href = True)
            if len(url2) > 0:
                if sc(url, "https://www.ptt.cc/hotboard.html") == True:
                    url3 = url2[0]
                    if sc(url3['href'], "bbs") > 0:
                        ExtractBoard("https://www.ptt.cc/bbs" + url3['href'].split("bbs")[1], boardinfo, p, 0)
                else:
                    for url3 in url2:
                        if  sc(url3['href'].split("bbs")[1], "1.html"):
                            continue   
def getimg(url, timeflag, count):
    
    res = req_loop(url, 0)
    #try:
    #    res = requests.get(url)
    #except:
    #    time.sleep(0.1)
    #    getimg(url, timeflag, count + 1)
        
    #print url
    soup = BeautifulSoup(res.text.encode("utf-8"))
    soup2 = soup.findAll("div", id = "main-container")
    if len(soup2) == 0:
        if count > 10:
            return False
        else:
            getimg(url, timeflag, count + 1)
    else:
        soup3 = soup2[0].findAll("a", href = True)
        for item in soup3:
            if sc(item.text.encode("utf-8"), "jpg"):
                sname = item.text.encode("utf-8").split("/")[3].split(".jpg")[0]
                print sname
                if (os.path.exists("./beauty/" + timeflag + "/%sjpg" % sname)):
                    continue#print item.text.encode("utf-8")
                else:
                    if os.path.exists("./beauty/" + timeflag.split("/")[0].replace(" ", "") + "_" + timeflag.split("/")[1]) == False:
                        os.mkdir("./beauty/" + timeflag.split("/")[0].replace(" ", "") + "_" + timeflag.split("/")[1])
                    if os.path.exists("./beauty/" + timeflag.split("/")[0].replace(" ", "") + "_" + timeflag.split("/")[1] + "/%s.jpg" % sname) == False:
                        try:
                            urllib.urlretrieve(item.text.encode("utf-8"),"./beauty/" + timeflag.split("/")[0].replace(" ", "") + "_" + timeflag.split("/")[1] + "/%s.jpg" % sname)
                        except:
                            time.sleep(0.5)
                            getimg(url, timeflag, count + 1)
                    time.sleep(0.1)
        
def getpage(url, thispage):
    print url
    
    res = req_loop(url, 0)
    if res == None:
        getpage("https://www.ptt.cc/bbs/Beauty/index" + str(thispage - 1) + ".html", thispage)
    #try:
    #    res = requests.get(url)
    #except:
    #    getpage(url, thispage, gpc + 1)
    soup = BeautifulSoup(res.text.encode("utf-8"))
    soup2 = soup.findAll("div", class_ = "r-ent")
    
    #soup2 = soup.findAll("span", class_ = "hl f1")
    for item in soup2:
        soup3 = item.findAll("span", class_ = "hl f3")
        
        if len(soup3) == 0:
            soup3 = item.findAll("span", class_ = "hl f1")
            if len(soup3) == 0:
                continue
        else:
            if int(soup3[0].text.encode("utf-8")) > 90:
                print int(soup3[0].text.encode("utf-8"))
            else:
                continue
        url1 = item.findAll('a', href = True)
        timeflag = item.find("div", class_="date").text.encode("utf-8")
        
        if len(url1) > 0:
            #print 
            print timeflag#print soup3
            getimg("https://www.ptt.cc/bbs" + str(url1[0]).split("/bbs")[1].split("\"")[0], timeflag, 0)
    nextpage = getboardindex(url, thispage, 0)
    print nextpage
    thispage = nextpage
    getpage("https://www.ptt.cc/bbs/Beauty/index" + str(nextpage) + ".html", thispage)
    time.sleep(0.1)
if __name__ == '__main__':
    if os.path.exists("./beauty") == False:
        os.mkdir("./beauty")
    getpage("https://www.ptt.cc/bbs/Beauty/index.html", 0)
        #soup3 = soup.findAll("span", class_ = "hl f3")
        
    #url = re.findall('(?<=href=").*(?=\">&lsaquo)', indexhtml)
    