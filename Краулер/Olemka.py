def csv_write(path, author, header, created, topic, source, publ_year, doc_counter):
    fir_row = ['path', 'author', 'sex', 'birthday', 'header', 'created', 'sphere', 'genre_fi',  #all headers
    'type', 'topic', 'chronotop', 'style', 'audience_age', 'audience_level', 'audience_size',
    'source', 'publication', 'publisher', 'publ_year', 'medium', 'country', 'region', 'language']
    info_row = [path, author, '', '', header, created, 'публистика', '', '', topic, '', 'нейтральный',  #info
    'н-возраст', 'н-уровень', 'районная', source, 'Олёмка', '', publ_year, 'газета', 'Россия',
    'Якутия', 'ru']
    with open('info.csv', 'a', newline = '', encoding = 'utf-8') as csv_f:
        csv_file = csv.writer(csv_f, delimiter = ',', quotechar = '|', 
            quoting = csv.QUOTE_MINIMAL)
        if doc_counter == 1:             #so that csv is only appended with first row once
            csv_file.writerow(fir_row)
        csv_file.writerow(info_row)

def find_author(tree):
    au_name_list = tree.xpath('.//em/strong/text()')
    for text in au_name_list:
        m = re.match('[А-Я]\.\s?([А-ЯЁ]|[а-яё])+', text) #selects author name from list
        if m:
            name = m.group()
            break
    if au_name_list == [] or m == None :
        name = 'Noname'         #asigns noname to name if no athor present
    return name


from lxml import html
import requests, os.path, sys, re, time, csv
try:                        #remove the csv file if it exists already, so it doesn't keep appending
    os.remove('info.csv')
except OSError:
    pass
href_skip = [] ## used for stiring visited sites
doc_counter = 1 ## used for creating ordinal file names
main_pg = requests.get("http://gazetaolekma.ru") ## input site here
tree = html.fromstring(main_pg.content)
hrefs = tree.xpath('//a[starts-with(@href, "http://gazetaolekma.ru") or starts-with(@href,"https://gazetaolekma.ru") or starts-with(@href,"ftp://gazetaolekma.ru")]/@href')  ## To avoid non-absolute hrefs
for href in hrefs:
    time.sleep(3) ##to be nice, and so I stop getting banned
    link_pg = requests.get(href)
    tree2 = html.fromstring(link_pg.content)
    if tree2.find('.//p') and tree2.find('.//*[@class="e-title"]') is not None and href not in href_skip:  ## If no text content (not an article), or site already visited, skips writing to text file
        doc_title = tree2.xpath('//*[@class="e-title"]/text()')  ## selects title of text from each link for file name
        clean_title = re.sub(r'(\?|\\|\?|\%|\*|\:|\|\||"|<|>)',r'',''.join(doc_title)) ##remove invalid chars
        theme = tree2.xpath('//span[@class="news-details-cat"]/a/text()')
        if theme == []:
            theme = 'Notopic'
        else:
            theme = theme[0]
        doc_content = str(tree2.xpath('.//p/text() | .//p/strong/text() | .//p/em/text() | .//p/.//span/text()')) ## extracts only text
        clean_doc_con = re.sub(r'((\', \')|\'|\\xa0|\\n|\[|\])',r'',''.join(doc_content))        ## remove unnecessary symbols
        au_name = find_author(tree2)
        date = tree2.xpath('//a[@class = "dateBar"]/text()')
        year = date[0]
        month = date[1]
        day = date[2]
        clean_date = "{0}.{1}.{2}".format(day, month, year)  #fromats date for writing in doc
        html_dir = os.path.join(os.getcwd(),"html\\{0}\\{1}".format(year, month))
        no_marks_dir = os.path.join(os.getcwd(),"no_marks\\{0}\\{1}".format(year, month))  
        if not os.path.exists(html_dir):  #creates nessesary directories if not already present
            os.makedirs(html_dir)
        if not os.path.exists(no_marks_dir):
            os.makedirs(no_marks_dir)
        with open("{0}/{1}.txt".format(html_dir, str(doc_counter)), "w", encoding = 'utf-8') as html_doc,\
        open("{0}/{1}.txt".format(no_marks_dir, str(doc_counter)), "w", encoding = 'utf-8') as no_marks_doc:
            html_doc.write(link_pg.text)
            no_marks_doc.write("@ {0}\n@ {1}\n@ {2}\n@ {3}\n@ {4}\n {5}".format(au_name, clean_title, clean_date, theme, href, clean_doc_con))
        csv_write(no_marks_dir, au_name, clean_title, clean_date, theme, href, year, doc_counter)
        doc_counter = doc_counter + 1
        href_skip.append(href) #appends list with already completed link
    hrefs2 = tree2.xpath('//a[starts-with(@href, "http://gazetaolekma.ru") or starts-with(@href,"https://gazetaolekma.ru") or starts-with(@href,"ftp://gazetaolekma.ru")]/@href')
    for href2 in hrefs2:
        if href2 not in hrefs:  #adds new links to search
            hrefs.append(href2)
