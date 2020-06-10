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
DML_URL_FORSEARCH = "https://www.dmm.co.jp/mono/dvd/-/search/=/searchstr=TESTTEST/"
class Car(object):
    car_url_forsearch = ""
    car_no_forseach =""
    car_no = []
    car_nm = []
    car_cover_url = []
    car_cover_file =""
    
    @classmethod
    def get_car_cover_ext(cls):
        # return "." + cls.car_cover_url.split(".")[-1]
        return ".jpg"
    
    @classmethod
    def get_car_no(cls):
        return cls.car_no
    
    @classmethod
    def get_car_url_forsearch(cls):
        return DML_URL_FORSEARCH.replace('TESTTEST', cls.car_no_forseach)
  
    @classmethod
    def get_car_cover_url(cls):
        return cls.car_cover_url
        
    @classmethod
    def get_car_nm(cls):
        return cls.car_nm
    
    @classmethod
    def __init__(cls, car_no_forseach):
        cls.car_no_forseach = car_no_forseach
        cls.car_url_forsearch = cls.get_car_url_forsearch()

    @classmethod
    def get_car_cover_info(cls):
        try:
            #get the url of dmm
            html = urllib.request.urlopen(cls.car_url_forsearch).read()
            soup = BeautifulSoup(html,'html.parser')
            car_info_rst = soup.find_all('p',{"class":"tmb"})
            #when come to several results
            for car_info in car_info_rst:
                car_info_url = 'http:' + str(car_info.find_all('span',{"class":"img"})[0].find('img')["src"])
                # filter 
                if filter_car_no(car_info_url, cls.car_no_forseach):
                    cls.car_cover_url.append(car_info_url)
                    cls.car_nm.append(car_info.find_all('span',{"class":"txt"})[0].text)
                    #todo
                    cls.car_no.append(car_info.find_all('span',{"class":"txt"})[0].text) 
        except Exception as e:
            logging.exception(e)

# match the pattern:
# starts with 3~5 letters and followed by numbers with or without Hyphen in front
def validated_car_no(car_no):
    regex = r'\w{2,5}\D*\d{1,5}$'
    return re.match(regex, car_no)

#car_no_forsearch is criticaly the substr of cover file name
def filter_car_no(car_url, key):
    car_file = car_url.split("/")[-1]
    # without - and all upercase
    return key.lower().replace("-","") in car_file

#download
def dl_car_cover(car):
    dl_as_file =  CAR_COVER_DL_DIR + "\\" + car.get_car_no() + car.get_car_cover_ext()
    for url in car.get_car_cover_url():
        urllib.request.urlretrieve(url, dl_as_file)
        

    
    
    
if __name__ == '__main__':
    args = sys.argv
    if  len(args) != 2:
        print("usage : python car.py car-no")
    else:
        car = Car(args[1])
        if validated_car_no(args[1]):
            car.get_car_cover_info()
            #print(car.get_car_nm()+" from "+car.get_car_cover_url()+"\n")
            print(car.get_car_url_forsearch())
            print(car.get_car_cover_url())
            #dl_car_cover(car)
        else:
            print("car-no is not properiate")
    
    
   
