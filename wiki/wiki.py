import os
import re
import codecs
import operator
fdic = {}

def extract():                                                                      #impliments WikiExtractor
    cmd = ("python WikiExtractor.py hawwiki-latest-pages-articles.xml.bz2")
    os.system(cmd)

def clean():
    with codecs.open("text/AA/wiki_00", "r", encoding = "utf8") as fil:
        with codecs.open("text/AA/wiki_cln.txt", "w", encoding = "utf8") as wrt:
            fil_cln = re.sub("<.*doc.*>","\n", fil.read())                          #get rid of extra xml doc tags
            wrt.write(fil_cln)

def freq():
    with codecs.open("text/AA/wiki_cln.txt", "r", encoding = "utf8") as fil:        #making a frequency list
        with codecs.open("text/AA/wiki_freq.txt", "w", encoding = "utf8") as wrt:
            no_punc = re.split("[^\w\d+]", fil.read())
            no_punc = list(filter(None, no_punc))
            for word in no_punc:
                try:
                    fdic[word] += 1
                except KeyError:
                    fdic[word] = 1
            sort_fdic = sorted(fdic.items(), key = operator.itemgetter(1), reverse = True)
            for k, v in sort_fdic:
                wrt.write("%s: %s\n"%(k,v))
    

extract()
clean()
freq()