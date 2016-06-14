import requests
import itertools
import csv
import os
import re
import json
from lxml import html


def rem ():
    try:
        os.remove('event_info.csv')
    except OSError:
        pass


def hrefs (d,m,y,pg):
    site = requests.get('http://cult.mos.ru/events/?date=%s.%s.%s&PAGEN_1=%s'%(d, m, y, pg))
    tree = html.fromstring(site.content)
    links = tree.xpath('//a[@class="b-article__link"]/@href')
    date = "%s.%s.%s"%(d, m, y)
    return {date: links}


def max_pg(d,m,y,pg):
    site = requests.get('http://cult.mos.ru/events/?date=%s.%s.%s&PAGEN_1=%s'%(d, m, y, pg))
    tree = html.fromstring(site.content)
    if tree.xpath('//a[@class="b-pages__item__link"]'):
        max_p = tree.xpath('//a[@class="b-pages__item__link"]/text()| //a[@class="b-pages__item__link"]/b/text()')[-1]
        # except IndexError:
        #     max_p = tree.xpath('//a[@class="b-pages__item__link"]/text()')[0]
    else:
        max_p = None
    return max_p


def incr (d,m,y,pg,max_p):
    try:
        max_p, pg = int(max_p), int(pg)
    except TypeError:
        pass
    if max_p is pg or max_p is None:
        if m in (1, 3, 5, 7, 9, 11):
            if d == 31:
                d = 0
                m += 1
        elif m == 2:
            if (y == 2016 and d == 29) or d == 28:
                d = 0
                m += 1
        else:
            if d == 30:
                d = 0
                if m == 12:
                    y += 1
                    m = 1
                else:
                    m += 1
        d += 1
        pg = 1
    else:
        pg += 1
    return (d,m,y,pg)


def extract (href_list):
    done = {}
    print ("Beginning information extraction...")
    first = False
    for dic in href_list:
        for date, link_list in dic.items():
            for link in link_list:
                if link not in done:
                    done[link] = [date]
                else:
                    done[link].append(date)
    for link,v in done.items():
        new_link = 'http://cult.mos.ru' + link
        if new_link != 'http://cult.mos.ru/free/':
            date = v[0:len(v)]
            date = ', '.join(date)
            eventpg = requests.get(new_link)
            tree = html.fromstring(eventpg.content.decode('utf-8'))
            text = tree.xpath('//div[@class="b-under-content b-text-content sm-text"]/div/text() | //div[@class="b-under-content b-text-content sm-text"]/a/text() | \
                //div[@class="b-under-content b-text-content sm-text"]/p/text() | //div[@class="b-under-content b-text-content sm-text"]/text()')
            text = ' '. join(text[0:len(text)])
            clean_text = re.sub('((\', \')| ,|\'|\\ x a 0|\\n|\[|\]|\|)',r'', text) 
            clean_text = re.sub(r'\s\s+',r'', clean_text) 
            try:
                event = tree.xpath('//h1[@class="xxxl-text font-bold"]/text()')[0]
            except IndexError:
                event = 'N/A'
            try:
                loc = tree.xpath('//span[@class="m-text"]/a/b/text()')[0]
            except IndexError:
                loc = 'N/A'
            try:
                st = tree.xpath('//span[@class="m-text"]/span[@class="color-gray"]/text() | //p/span[@class="color-gray"]/text()')[0]
                st = re.sub(r'\s\s+',r'', st) 
            except IndexError:
                st = 'N/A'
            cat = tree.xpath('//a[@class="b-bread-crumbs__item color-red"]/b/text()')
            cat = cat[0:len(cat)]
            cat = ' '.join(cat)
            try:
                price = tree.xpath('//div[@class="b-gray-blocks__content b-text-content"]/p/text() | //div[@class="b-gray-blocks__content b-text-content"]/p/span[@class="m-text"]/text()')[0]
                if re.search(r'^\s\s+$', price):
                    price = tree.xpath('//div[@class="b-gray-blocks__content b-text-content"]/p/text()')[1]
            except IndexError:
                price = 'N/A'
            csv_write(new_link, clean_text, event, loc, st, date, cat, price, first)
            first = True

def csv_write (link, text, event, loc, st, date, cat, price, first):
    first_row = ['link', 'text', 'event', 'location', 'street', 'date', 'category', 'price']
    info_row = [link, text, event, loc, st, date, cat, price]
    with open('event_info.csv', 'a', encoding = 'utf-8') as csv_f:
        csv_file = csv.writer(csv_f, delimiter = '\t', quotechar = '|',
            quoting = csv.QUOTE_MINIMAL)
        if first == False:
            csv_file.writerow(first_row)
        csv_file.writerow(info_row)

rem()
# print ("Prior csv file removed.")
# d = 1
# m = 2
# y = 2014
# pg = 1
# href_list = []
# print ("Beginning href extraction...")
# while y <= 2015 or (m < 6 and y <= 2016):
#     href_list.append(hrefs(d,m,y,pg))
#     if pg == 1:
#         max_p = max_pg(d,m,y,pg)
#     print ("%s.%s.%s   pg:%s"%(d,m,y,pg))
#     incr_tup = incr(d,m,y,pg, max_p)
#     d = incr_tup[0]
#     m = incr_tup[1]
#     y = incr_tup[2]
#     pg = incr_tup[3]
# with open('links.json', 'w') as hrefs:
#     hrefs.write(json.dumps(href_list))
with open('links.json', 'r') as hrefs:
    href_list = hrefs.read()
    href_list = json.loads(href_list)
extract(href_list)
print ("Program Complete.")