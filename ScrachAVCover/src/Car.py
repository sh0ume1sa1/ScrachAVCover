r"""
update 2020/06/01 Refactoring
"""

__author__ = 'sai.sm'


from bs4 import BeautifulSoup
# -*- coding: utf-8 -*-
import urllib.request
import re,sys
import logging

CAR_COVER_DL_DIR = "..\\cover"
TARGET_CAR_LIST = ".\\res\\target.json"
DML_URL_FORSEARCH = "http://www.dmm.co.jp/rental/monthly/-/search/" \
                "=/searchstr=TESTTEST/floor=dvd/"
class Car():
    car_url_forsearch = ""
    car_no = ""
    car_nm = ""
    car_cover_url = ""
    car_cover_ext =""
    
    @classmethod
    def get_car_cover_ext(cls):
        return "." + cls.car_cover_url.split(".")[-1]
    
    @classmethod
    def get_car_no(cls):
        return cls.car_no
    
    @classmethod
    def get_car_url_forsearch(cls):
        return DML_URL_FORSEARCH.replace('TESTTEST', cls.car_no)
            
    @classmethod
    def __init__(cls, car_no):
        cls.car_no = car_no
        cls.car_url_forsearch = cls.get_car_url_forsearch()

    @classmethod
    def get_car_cover_url(cls):
        try:
            #get the url of dmm
            html = urllib.request.urlopen(cls.car_url_forsearch).read()
            soup = BeautifulSoup(html,'html.parser')
            car_info = soup.findAll('p',{"class":"tmb"})
            cls.car_cover_url='http:' + str(car_info[0].find_all('span',{"class":"img"})[0].find('img')["src"])
            cls.car_nm = car_info[0].findAll('span',{"class":"txt"})[0].text
        except Exception as e:
            logging.exception(e)

    # match the pattern :
    # starts with 3~5 letters and followed by numbers with or without Hyphen in front
    @classmethod
    def validated_car_no(cls):
        regex = r'\w{2,5}\D*\d{1,5}$'
        if not(re.match(regex, cls.car_no)):
            print (cls.car_no +" not matches!")
            return False
        return True

def dl_car_cover(cls):
    dl_as_file =  CAR_COVER_DL_DIR + "//" + car.get_car_no() + car.get_car_cover_ext()
    
    urllib.request.urlretrieve(c., dl_as_file)
    

if __name__ == '__main__':
    args = sys.argv
    print(len(args))
    if  len(args) != 2:
        print("usage : python car.py car-no")
    else:
        car = Car(args[1])
        #print(args[1], car.car_url_forsearch)
        if car.validated_car_no():
            car.get_car_cover_url()
            print(car.car_nm, car.car_cover_url)
            
            #urllib.request.urlretrieve(cover_url, car.dl_as_file)
        else:
            print("car-no is not properiate")
    
    
   
