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
COMMON_HEAD = "https://www.opensubtitles.org/en/"
TARGET_MOVIE_LIST = ".\\res\\movie_target.json"
GMAIL ="kayomii2678@gmail.com"
SUB_URL_FORSEARCH = "https://www.opensubtitles.org/libs/suggest.php?format=json3&MovieName=TESTTEST%20&SubLanguageID=jpn"
SUB_URL ="https://www.opensubtitles.org/en/subtitleserve/sub/SUBID"
MOVIE_URL = "https://www.opensubtitles.org/en/search/sublanguageid-jpn/idmovie-MOVIEID"
MAIL_TXT ="あなたが待ちに待ったサブタイトル:%s が\nありました! ダウンロードアドレス：%s\n ミー"

class Subtitle(object):
    movie_title =""
    movie_year =""
    sub_url_forsearch =""
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
            movie_object['lastFound'] = str(datetime.date.today())
            movie_object['subList'] = cls.get_sub_info(movie_object['movie_url'])
        cls.movie_target.append(movie_object)
    
    @classmethod
    def get_movie_info(cls):
        try:
            r_get = requests.get(cls.sub_url_forsearch)
            movies_info = json.loads(r_get.text)
            
            for movie_info in movies_info: 
                if (cls.movie_year != ''):
                    if (movie_info['year'] == cls.movie_year):
                        cls.set_movie_object(movie_info)
                else:
                    cls.set_movie_object(movie_info)
                    
            #print(cls.movie_target)
        except Exception as e:
            logging.exception(e)
    
    @classmethod
    def get_sub_info(cls, move_url):
        rtn=[]
        print(COMMON_HEAD+move_url)
        html = urllib.request.urlopen(COMMON_HEAD+move_url).read()
        soup = BeautifulSoup(html,'html.parser')
        all_sub = soup.find_all('tr',id=re.compile(r'^name\d{7}$')) #nameXXXXXXX subid 7 digital
        for one_sub in all_sub:
            sub_id = one_sub.find_all('td')[0]['id']
            subName = one_sub.find_all('td')[0].text
            uploadYmd = one_sub.find_all('td')[3].find('time').text
            subUrl = one_sub.find_all('td')[4].find('a')['href']
            rating = one_sub.find_all('td')[5].find('span').text + '/' + one_sub.find_all('td')[5].find('span')['title']
            single_sub = {
            	  "subName": subName,
                "rating":rating,
                "uploadYmd":uploadYmd,
                "subUrl":subUrl
                }
            print(single_sub)
        rtn = rtn.append(single_sub)
        return rtn
                      
    @classmethod
    def get_sub_url_forsearch(cls):
        return SUB_URL_FORSEARCH.replace('TESTTEST', cls.movie_title)
  
    @classmethod
    def __init__(cls, movie_title, movie_year=''):
        cls.movie_title = movie_title
        cls.movie_year = movie_year
        cls.sub_url_forsearch = cls.get_sub_url_forsearch()
        
    def send_mail(self):
        print("send mail")
        
    def edit_target(self,cls):
        print("send mail")
        
if __name__ == '__main__':
    args = sys.argv
    if  len(args) <=1:
        print("usage : python Waitsub.py movie-name [movie-year]")
    else:
        sub = Subtitle(args[1], args[2] if len(args)>=3 else '')
        sub.get_movie_info()
        #urllib.request.urlretrieve(SUB_URL_DOWLOAD,SUB_DL_DIR )

    
    
   
