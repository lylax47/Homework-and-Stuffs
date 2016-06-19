import re
import os
from lxml import etree
from nltk.tokenize import sent_tokenize
from xml.dom import minidom



def comp(auth):
    final = []
    for root, dirs, files in os.walk(auth):
        for name in files:
            tree = etree.parse(os.path.join(root, name))
            sents = tree.xpath('//se[@lang = "uk"]/text()')
            for sent in sents:
                final.append(sent)
    return final



def rus_comp(auth):
    final = []
    for root, dirs, files in os.walk(auth):
        for name in files:
            tree = etree.parse(os.path.join(root, name))
            sents = tree.xpath('//se[@lang = "ru"]/text()')
            for sent in sents:
                final.append(sent)
    return final



def rep(templ, samp):
    new_samp = []
    si1 = 0
    si2 = 0
    while si1 <= (len(templ) - 1):
        sent1 = str(templ[si1])
        sent2 = str(samp[si2])
        tok1 = sent_tokenize(sent1)
        tok2 = sent_tokenize(sent2)
        tokl1 = len(tok1)
        tokl2 = len(tok2)
        # if sent1[0] != sent2[0]:
        #     si2 -= 1
        #     si1 += 1
        #     pass
        if tokl1 == tokl2:
            new_samp.append(sent1)
        elif tokl1 > 2:
            tok_n = ''.join(tok1[0:1])
            new_samp.append(tok_n)
            new_samp.append(tok1[2])
            si2 += 1    
        elif tokl1 > tokl2:
            new_samp.append(tok1[0])
            new_samp.append(tok1[1])
            si2 += 1
        else:
            sent1 = tok1[0]
            si1 += 1
            try:
                sent2 = str(templ[si1])
            except IndexError:
                print(si1)
                break
            sent_comb = sent1 + sent2
            new_samp.append(sent_comb)
        si1 += 1
        si2 += 1
    return new_samp



def xml_write(sent_list, ru_list, run):
    i = 0
    root = etree.Element('root')
    page = etree.SubElement(root, 'html')
    headElt = etree.SubElement(page, 'head')
    bodyElt = etree.SubElement(page, 'body')
    for sent_en, sent_ru in zip(sent_list, ru_list):
        paraElt = etree.SubElement(bodyElt, 'para', id = str(i))
        seElt = etree.SubElement(paraElt, 'se', lang = 'en', variant_id = '0')
        seElt.text = sent_en
        seElt2 = etree.SubElement(paraElt, 'se', lang = 'ru', variant_id = '1')
        seElt2.text = sent_ru
        i += 1
    if run == False:
        name = 'Iljin'
    else:
        name = 'Nosik'
    xmlstr = minidom.parseString(etree.tostring(root)).toprettyxml(indent="   ")
    with open('{0}.xml'.format(name), 'w', encoding = 'utf-8') as xml_doc:
        xml_doc.write(xmlstr)
    run = True
    return run



tree = etree.parse('pnin_barabtarlo.xml')
orig_sents = tree.xpath('//se[@lang = "en"]/text()')
iljin = comp("iljin")
nosik = comp("nosik")
iljin_ru = rus_comp('iljin')
nosik_ru = rus_comp('nosik')
iljin_new = rep(orig_sents, iljin)
nosik_new = rep(orig_sents, nosik)
print(len(iljin_ru))
print(len(iljin_new))
print(len(nosik_ru))
print(len(nosik_new))
run = False
run = xml_write(iljin_new, iljin_ru, run)
xml_write(nosik_new, nosik_ru, run)