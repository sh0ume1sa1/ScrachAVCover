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
TARGET_MOVIE_LIST = ".\\res\\movie_target.json"
GMAIL ="kayomii2678@gmail.com"
SUB_URL_FORSEARCH = "https://www.opensubtitles.org/libs/suggest.php?format=json3&MovieName=TESTTEST%20&SubLanguageID=jpn"
class Subtitle(object):
    movie_title =""
    sub_url_forsearch =""
    @classmethod
    def get_subtitle(cls):
        try:
            r_get = requests.get(cls.sub_url_forsearch)
            subs = json.loads(r_get.text)
            for sub in subs: 
                print(sub['name']+':'+sub['year'] + ' '+sub['total']+' sub(s)')
        except Exception as e:
            logging.exception(e)
            

    
    @classmethod
    def get_sub_url_forsearch(cls):
        return SUB_URL_FORSEARCH.replace('TESTTEST', cls.movie_title)
  
   
    @classmethod
    def __init__(cls, movie_title):
        cls.movie_title = movie_title
        cls.sub_url_forsearch = cls.get_sub_url_forsearch()


if __name__ == '__main__':
    args = sys.argv
    if  len(args) != 2:
        print("usage : python Waitsub.py movie-name")
    else:
        sub = Subtitle(args[1])
        sub.get_subtitle()

    
    
   
