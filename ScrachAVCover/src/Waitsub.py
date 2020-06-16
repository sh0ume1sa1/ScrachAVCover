r"""
wait sub
search sub of jpn on opensubtitile.org
menu:
1. add a new movie
2. list sub
"""

__author__ = 'sai.sm'


from bs4 import BeautifulSoup
# -*- coding: utf-8 -*-
import urllib.request
import requests
import json
import re,sys,logging
import datetime

SUB_DL_DIR = "..\\sub"
MOVIE_FOR_SEARCH = ".\\res\\movie_for_search.json"
GMAIL =""
MAIL_TITLE ="あなたがほしい字幕ができました！"
MAIL_TXT ="映画: %s "
COMMON_HEAD="https://www.opensubtitles.org/en/"
SUB_URL_FORSEARCH="https://www.opensubtitles.org/libs/suggest.php?format=json3&MovieName=TESTTEST&SubLanguageID=jpn"
SUB_URL="https://www.opensubtitles.org/en/subtitleserve/sub/SUBID"
SUB_DL_URL="http://dl.opensubtitles.org/en/download/sub/SUBID"
MOVIE_URL="https://www.opensubtitles.org/en/search/sublanguageid-jpn/idmovie-MOVIEID"

class Subtitle(object):
    movie_title = ""
    movie_year = ""
    sub_url_forsearch = ""
    sub_file_name = []
    movie_target = []
    
    @classmethod
    def get_movie_object(cls):
        return {
            "id": "",
            "name": '',
            "year": '',
            "wanted": True,
            "movie_url": "search/sublanguageid-jpn/idmovie-MOVIEID",
            "found": False,
            "total": 0,
            "lastFound": "",
            "subList": []
        } 
    
    @classmethod
    def set_movie_object(cls,movie_info):
        movie_object = cls.get_movie_object()
        if (movie_info != []):
            movie_object['id'] = movie_info['name']+'-'+movie_info['year']
            movie_object['name'] = movie_info['name']
            movie_object['year'] = movie_info['year']
            movie_object['movie_url'] = movie_object['movie_url'].replace('MOVIEID',str(movie_info['id']))
            movie_object['found'] = True
            movie_object['total'] = movie_info['total']
            movie_object['lastFound'] = str(datetime.date.today())
            movie_object['subList'] = cls.get_sub_info(movie_object)
        cls.movie_target.append(movie_object)
    
    @classmethod
    def get_movie_info(cls):
        try:
            r_get = requests.get(cls.sub_url_forsearch)
            #print(cls.sub_url_forsearch)
            movies_info = json.loads(r_get.text)
            
            for movie_info in movies_info: 
                if (cls.movie_year != ''):
                    if (movie_info['year'] == cls.movie_year):
                        #print("===MOVIE NAME:",movie_info['name'],movie_info['year'],sep=' ')
                        cls.set_movie_object(movie_info)
                else:
                    #print("===MOVIE NAME:",movie_info['name'],movie_info['year'],sep=' ')
                    cls.set_movie_object(movie_info)
                    
            #print(cls.movie_target)
        except Exception as e:
            logging.exception(e)
    
    @classmethod
    def get_sub_info(cls, movie_object):
        rtn=[]
        movie_url = movie_object['movie_url']
        print(movie_object['name'],movie_object['total']+' subs')
        html = urllib.request.urlopen(COMMON_HEAD+movie_url).read()
        soup = BeautifulSoup(html,'html.parser')
        if (int(movie_object['total']) > 1):
            #more than one subtitile
            all_sub = soup.find_all('tr',id=re.compile(r'^name\d{3,9}$')) #nameXXXXXXX subid 3~7 digital
            for one_sub in all_sub:
                sub_id = one_sub.find_all('td')[0]['id'].replace('main','')
                subName = one_sub.find_all('td')[0].text.replace('Watch onlineDownload Subtitles Searcher','')
                uploadYmd = one_sub.find_all('td')[3].find('time').text.split("/")
                #subUrl = one_sub.find_all('td')[4].find('a')['href']
                subUrl = SUB_DL_URL.replace('SUBID', sub_id)
                try:
                    rating = one_sub.find_all('td')[5].find('span').text + '/' + one_sub.find_all('td')[5].find('span')['title']
                except:
                    rating = "no vote"
                single_sub = {
                    "subId": sub_id,
                    "subName": subName,
                    "rating":rating,
                    "uploadYmd":uploadYmd[2]+'/'+uploadYmd[1]+'/'+uploadYmd[0],
                    "subUrl":subUrl
                }
                #print(single_sub)
                rtn.append(single_sub)
        else:
            #only one subtitile, html rendered differently
            sub_id = soup.find('a',download='download')['data-product-id']
            #subUrl = soup.find('a',download='download')['href']
            subUrl = SUB_DL_URL.replace('SUBID', sub_id)
            
            subName = soup.find('a',download='download')['data-product-name']
            single_sub = {  
                  "subId": sub_id,
                  "subName": subName,
                  "rating":'0/0',
                  "uploadYmd":'uploadYmd',
                  "subUrl":subUrl
            }
            rtn.append(single_sub)
        #print(rtn)
        return rtn
                      
    @classmethod
    def get_sub_url_forsearch(cls):
        return SUB_URL_FORSEARCH.replace('TESTTEST', cls.movie_title.replace(' ','%20'))
  
    @classmethod
    def __init__(cls, movie_title, movie_year=''):
        cls.movie_title = movie_title
        cls.movie_year = movie_year
        cls.sub_url_forsearch = cls.get_sub_url_forsearch()
        
def send_mail(sub):
    for m in sub.movie_target:
        print(m['name'],m['year'])
        for s in m['subList']:
            print("--- ",s['subName'].replace('\n',' '))
            print("---","uploaded on:",s['uploadYmd'],"rating:", s['rating'],s['subUrl'])
                  
if __name__ == '__main__':
    args = sys.argv
    if  len(args) <=1:
        #print("usage : python Waitsub.py movie-name [movie-year]")
        #movie_for_search.jsonを読み込み
        with open(MOVIE_FOR_SEARCH) as json_file:
            movie_for_search_all = json.load(json_file)
            for m in movie_for_search_all:
                if (m['wanted']):
                    sub = Subtitle(m['name'], m['year'])
                    sub.get_movie_info()
                    if (sub.movie_target != []):
                        send_mail(sub)
                    else:
                        print("no results")
            
    else:
        #command line for test
        sub = Subtitle(args[1], args[2] if len(args)>=3 else '')
        sub.get_movie_info()
        print(sub.movie_target)
        

    
    
   
