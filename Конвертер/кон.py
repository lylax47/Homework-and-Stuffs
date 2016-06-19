import os
import re
import csv
import xml.etree.ElementTree as ET
from lxml import etree, html
from xml.dom import minidom


def rem ():
    try:
        os.remove('convert.txt')
    except OSError:
        pass

def get_para():
    path = input('Введите путь к файлу или название, если файл находится в этой папке:')
    if not os.path.exists(path):
        while not os.path.exists(path):
            print('\nДанный путь не существует.\n') 
            path = input('Введите путь к файлу или название, если файл находится в этой папке:') 
    form = input('Введите конечный формат(xhtml или prs):')
    if form not in ['xhtml', 'prs']:
        while form not in ['xhtml', 'prs']:
            print('\nВы не правильно встваили формат.\n')
            form = input('Введите "xhtml" или "prs":')
    return (path, form)



def xhtml_ex(path):
    info_list = []
    tree = etree.parse(path)
    sents = tree.xpath('.//se')
    i = 0
    for sent in sents:
        i += 1
        sentno = i
        words = sent.xpath('.//w')
        c = 0
        for w in words:
            sen_len = len(sent)
            c += 1
            if c == 1:
                sent_pos = 'bos'
            elif c == sen_len:
                sent_pos = 'eos' 
            else:
                sent_pos = ''  
            wordno = c
            word = w.xpath('text()')[-1]
            word = word.strip()
            anas = w.xpath('.//ana')
            nvars = len(anas)
            nvar = 1
            if re.match('[А-Я]\S+', word):
                graph = 'cap'
            else:
                graph = ''
            for ana in anas:
                lem = str(ana.xpath('@lex')[0])
                lex = str(re.sub('(,?[a-z1-9,?.?]+)', '', ana.xpath('@gr')[0]))
                gram = str(re.sub('([A-Z],)', '', ana.xpath('@gr')[0]))
                trans = str(ana.xpath('@trans')[0])
                if ana.xpath('@morph') == 'Ø':
                    nlems = '1'
                else:
                    nlems = '2'
                info_list.append([str(sentno), str(wordno), graph, word, str(nvars), str(nlems), str(nvar), lem, trans, lex, gram, sent_pos])
                nvar += 1         
            
        
    return info_list


def to_prs(info_list):
    run1 = False
    fir_row = ['#sentno', '#wordno', '#graph', '#word', '#nvars', '#nlems', '#nvar', '#lem', '#trans', '#lex', '#gram', '#sent_pos']
    file_name = 'convert.txt'
    with open(file_name, 'a', newline = '', encoding = 'utf-8') as tsvfile:
        prsfile = csv.writer(tsvfile, delimiter = '\t')
        for row in info_list:
            if run1 == False:
                prsfile.writerow(fir_row)
                run1 = True
            prsfile.writerow(row)
    return file_name


def prs_ex(path):
    data_list = []
    with open('{0}'.format(path), 'r', encoding = 'utf-8') as tsvfile:
        tsvread = csv.reader(tsvfile, delimiter = '\t')

        run1 = False
        for row in tsvread:
            if run1 == False:
                run1 = True
            elif re.match('#meta([.*]+)', row[0]):
                pass
            else:
                data_list.append(row)
    return (data_list)


def to_xml(data_list):
    pre_word = ''
    root = etree.Element('root')
    doc = etree.SubElement(root, 'doc')
    body = etree.SubElement(doc, 'body')
    for row in data_list:
        if row[1] == '1' and row[4] != pre_word:
            seElt = etree.SubElement(body, 'se')
        if row[8] == '1':
            wElt = etree.SubElement(seElt, 'w')
            wElt.text = row[4]
            if row[16] != '':
                wElt.tail = row[16].replace(r'\n', '')
        morpho = re.sub(row[9], '', row[4].lower())
        if morpho == '':
            morpho = 'Ø'
        anaElt = etree.SubElement(wElt, 'ana', lex = row[9], morph = morpho, \
            gr = ('{0}, {1}'.format(row[12], row[13])), trans = row[10])
        pre_word = row[4]
    xmlstr = minidom.parseString(etree.tostring(root)).toprettyxml(indent="   ")
    file_name = 'convert.xml'
    with open(file_name, 'w', encoding = 'utf-8') as xml_doc:
        xml_doc.write(xmlstr)
    return file_name



tup = get_para()
if tup[1] in 'prs':
    rem()
    xml_info = xhtml_ex(tup[0])
    name = to_prs(xml_info)
    print('\n' + 'Directory:   ' + os.getcwd() + name)
else:
    prs_info = prs_ex(tup[0])
    name = to_xml(prs_info)
    print('\n' + 'Directory:   ' + os.getcwd() + name)
