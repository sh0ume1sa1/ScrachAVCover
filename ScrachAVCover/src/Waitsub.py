r"""
wait sub
"""

__author__ = 'sai.sm'


from bs4 import BeautifulSoup
# -*- coding: utf-8 -*-
import urllib.request
import requests
import json
import sys,logging

SUB_DL_DIR = "..\\sub"
SUB_LAN = "jpn"
TARGET_MOVIE_LIST = ".\\res\\movie_target.json"
GMAIL ="kayomii2678@gmail.com"
SUB_URL_FORSEARCH = "https://www.opensubtitles.org/libs/suggest.php?format=json3&MovieName=TESTTEST%20&SubLanguageID="+SUB_LAN
SUB_URL_DOWLOAD ="https://www.opensubtitles.org/en/subtitleserve/sub/8150232"
MAIL_TXT ="あなたが待ちに待ったサブタイトル:%s が\nありました! ダウンロードアドレス：%s\n ミー"

class Subtitle(object):
    movie_title =""
    sub_url_forsearch =""
    sub_file_name = []
    
    @classmethod
    def get_subtitle(cls):
        try:
            r_get = requests.get(cls.sub_url_forsearch)
            subs = json.loads(r_get.text)
            for sub in subs: 
                print(sub['name']+':'+sub['year'] + ' '+sub['total']+' sub' + ('' if sub['total']=='1' else 's'))
        except Exception as e:
            logging.exception(e)
            

    
    @classmethod
    def get_sub_url_forsearch(cls):
        return SUB_URL_FORSEARCH.replace('TESTTEST', cls.movie_title)
  
   

    def __init__(self, movie_title):
        self.movie_title = movie_title
        self.sub_url_forsearch = self.get_sub_url_forsearch()
        
    def send_mail(self):
        print("send mail")
        
    def edit_target(self,cls):
        print("send mail")
        
if __name__ == '__main__':
    args = sys.argv
    if  len(args) != 2:
        print("usage : python Waitsub.py movie-name")
    else:
        sub = Subtitle(args[1])
        print(MAIL_TXT,'adsasd','dsfsdf')
        sub.get_subtitle()
        urllib.request.urlretrieve(SUB_URL_DOWLOAD,SUB_DL_DIR )

    
    
   
