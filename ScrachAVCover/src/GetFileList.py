r"""
this is the program that can scratch the cover from
www.dmm.co.jp by the banngou like "YRZ003" in a certain
directory in your computer
written at 2013/06/11 ver 0.1
updated at 2014/03/20 ver 0.2
updated at 2014/10/25 fix [cover is not available on web] error
"""

__author__ = 'jimmy'

from BeautifulSoup import BeautifulSoup
# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
from os import listdir
from os.path import isfile, join,exists
DMMSEARCH = "http://www.dmm.co.jp/search/=/searchstr=TESTTEST/analyze=V1EBCFcEUAU_/" \
            "n1=FgRCTw9VBA4GF1RWR1cK/n2=Aw1fVhQKX0BdC0VZX2kCQQU_/sort=ranking/"
#TARGETDIR = "h:\\xxx\\--!!!!!!t0d@y"
TARGETDIR = "z:\\video\\00_AV"
#http://www.dmm.co.jp/search/=/searchstr=jbs007/analyze=V1EBClcEUQU_/n1=FgRCTw9VBA4GF1RWR1cK/n2=Aw1fVhQKX0BdC0VZX2kCQQU_/sort=ranking/

def getCoverImage(url):
    print '[url=]'+url
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    result = soup.findAll(href=re.compile("pics\.dmm\.co\.jp"))
    try:
        return str(result[0]).split('"')[1]
    except BaseException:
        return ""


def getAccurateUrl(avCode):
    postUrl = DMMSEARCH.replace('TESTTEST', avCode)
    try:
        #get the url of dmm
        print "[AVcode]"+avCode
        html = urllib2.urlopen(postUrl).read()
        soup = BeautifulSoup(html)
        result = soup.findAll(href=re.compile("detail"))
        #print result
        return str(result[0]).split('"')[1]
    except urllib2.HTTPError:
        return ""


def checkAvCode(avCode, i='*'):
    # match the pattern :
    # starts with 3~5 letters and followed by numbers with or without Hyphen in front
    regex = r'\w{2,5}\D*\d{1,5}\.(.*)$'
    if not(re.match(regex, avCode)):
        #print avCode + " matches"

        print "No." + str(i) + " " + avCode + " not matches!"
        return False
    return True



def readFileIntoList(path):
    #scratch file name into a list under a certain dir
    return [f for f in listdir(path) if isfile(join(path,f))]


for ele in readFileIntoList(TARGETDIR):
        if checkAvCode(str(ele)):
            avCode = str(ele).split(".")[0]
            coverUrl = getAccurateUrl(avCode)
            if coverUrl != "":
                coverUrl = getCoverImage(coverUrl)
                downLoadAs = TARGETDIR + '\\' + avCode + '.jpg'
                # if file already exists
                if exists(downLoadAs):
                    print 'Cover for ' + avCode + ' is already exists'
                else:
                    print '[cc]'+coverUrl
                    if coverUrl != "":
                        data = urllib.urlretrieve(coverUrl, downLoadAs)
                        print "Cover for " + avCode + " OK!\n"
                    else:
                        print "Cover for " + avCode + " N/A \n"
            else:
                print "Not found the cover for " + avCode + "\n"

                print "test is not a null is not cally "
