from lxml import html
import requests, os.path, sys, re
spath = os.path.dirname(sys.argv[0])  ## finds path of script
main_pg = requests.get("http://gazetaolekma.ru/") ## input site here
with open(os.path.join(spath, "Main.txt"),"w", encoding='utf-8') as doc: 
    doc.write(main_pg.text)
tree = html.fromstring(main_pg.content)
hrefs = tree.xpath('//a[starts-with(@href, "http:") or starts-with(@href,"https:") or starts-with(@href,"ftp:")]/@href')  ## To avoid non-absolute hrefs
for href in hrefs:
    link_pg = requests.get(href)
    tree2 = html.fromstring(link_pg.content)
    doc_title = tree2.xpath('//html/head/title/text()')  ## selects title of text from each link
    file_name = re.sub(ur'(\?|\\|\?|\%|\*|:\||"|<|>)',ur'',''.join(doc_title)) ##remove invalid chars
    with open(os.path.join(spath, "%s.txt"%file_name), "w", encoding ='utf-8') as href_doc:
        href_doc.write(link_pg.text)