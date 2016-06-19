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
    site = requests.get('http://www.2do2go.ru/msk/events?date=%s-%s-%s&page=%s'%(d, m, y, pg))
    tree = html.fromstring(site.content)
    links = tree.xpath('//a[@class="medium-events-list_link"]/@href')
    date = "%s.%s.%s"%(d, m, y)
    return {date: links}


def max_pg(d,m,y,pg):
    site = requests.get('http://www.2do2go.ru/msk/events?date=%s-%s-%s&page=%s'%(d, m, y, pg))
    tree = html.fromstring(site.content)
    if tree.xpath('//a[@class="paginator_link"]'):
        max_p = tree.xpath('//a[@class="paginator_link"]/text()')[-2]
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
        date = v[0:len(v)]
        date = ', '.join(date)
        eventpg = requests.get(link)
        tree = html.fromstring(eventpg.content.decode('utf-8'))
        text = tree.xpath('.//p/text() | .//p/strong/text() | .//p/em/text() | .//p/span/text() | .//p/a/text()')
        text = text[0:len(text) - 4]
        text = ' '. join(text)
        clean_text = re.sub(r'((\', \')| ,|\'|\\ x a 0|\\n|\[|\]|\||)',r'', text) 
        event = tree.xpath('.//h1[@itemprop="name"]/text()')[0]
        try:
            loc = tree.xpath('//a[@class="event-schedule_place-link"]/text()')[0]
        except IndexError:
            loc = 'N/A'
        st = tree.xpath('//div[@class="event-schedule_street"]/text()')[0]
        try:
            dur = tree.xpath('//div[@class="event-schedule_duration"]/text()')[0]
            dur = re.sub(r'Длительность:',r'', dur)
        except IndexError:
            dur = 'N/A'
        cat = tree.xpath('//div[@class="event-info_labeled js-categories-list"]/.//a/text()')
        cat = cat[0:len(cat)]
        cat = ' '.join(cat)
        price = tree.xpath('//div[@class="form-inline"]/text()')[0]
        views = tree.xpath('//div[@class="counters_item counters_item__views"]/text()')[0]
        comm = tree.xpath('//a[@class="counters_item counters_item__comments"]/text()')[0]
        csv_write(link, clean_text, event, loc, st, date, dur, cat, price, views, comm, first)
        first = True

def csv_write (link, text, event, loc, st, date, dur, cat, price, views, comm, first):
    first_row = ['link', 'text', 'event', 'location', 'street', 'date', 'duration', 'category', 'views', 'comments']
    info_row = [link, text, event, loc, st, date, dur, cat, views, comm]
    with open('event_info.csv', 'a', encoding = 'utf-8') as csv_f:
        csv_file = csv.writer(csv_f, delimiter = ';')
        if first == False:
            csv_file.writerow(first_row)
        csv_file.writerow(info_row)

rem()
# print ("Prior csv file removed.")
# d = 1
# m = 1
# y = 2013
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
with open('links.json', 'r') as hrefs:
    href_list = hrefs.read()
    href_list = json.loads(href_list)
extract(href_list)
print ("Program Complete.")
