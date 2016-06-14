import requests
import itertools
import csv
import os
import re
import json
from lxml import html




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
        cat = tree.xpath('//div[@class="event-info_labeled js-categories-list"]/.//a/text()')
        cat = cat[0:len(cat)]
        cat = ' '.join(cat)
        price = tree.xpath('//div[@class="form-inline"]/text()')[0]
        views = tree.xpath('//div[@class="counters_item counters_item__views"]/text()')[0]
        comm = tree.xpath('//a[@class="counters_item counters_item__comments"]/text()')[0]
        csv_write(link, clean_text, event, loc, st, date, cat, price, views, comm, first)
        first = True

def csv_write (link, text, event, loc, st, date, cat, price, views, comm, first):
    first_row = ['link', 'text', 'event', 'location', 'street', 'date', 'category', 'price', 'views', 'comments']
    info_row = [link, text, event, loc, st, date, cat, price, views, comm]
    with open('event_info.csv', 'a', encoding = 'utf-8') as csv_f:
        csv_file = csv.writer(csv_f, delimiter = '\t', quotechar = '|',
            quoting = csv.QUOTE_MINIMAL)
        if first == False:
            csv_file.writerow(first_row)
        csv_file.writerow(info_row)


with open('links.json', 'r') as hrefs:
    href_list = hrefs.read()
    href_list = json.loads(href_list)
extract(href_list)
print ("Program Complete.")
