import os
import re
import codecs
import operator

def extract():                                                                      #impliments WikiExtractor
    cmd = ("python WikiExtractor.py kywiki-20160501-pages-articles-multistream")
    os.system(cmd)

def clean():
    with codecs.open("text/AA/wiki_00", "r", encoding = "utf8") as fil:
        with codecs.open("text/AA/wiki_cln.txt", "w", encoding = "utf8") as wrt:
            fil_cln = re.sub("<.*doc.*>","\n", fil.read())                          #get rid of extra xml doc tags
            wrt.write(fil_cln)


extract()
#clean()