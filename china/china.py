import re
import io
from lxml import etree
from xml.dom import minidom



def make_dic(dic):
	long_word_dic = {}
	lines = dic.split('\n')
	for line in lines:
		if line[0] != '#':
			sent = line.split(' ')
			word = sent[1]
			inton_ser = re.search('\[([^]]+)\]', line)
			mean_ser = re.search('\/(.*)\/', line)
			inton = inton_ser.group(1)
			mean = mean_ser.group(1).replace('/', ', ')
			if word in long_word_dic.keys():
				long_word_dic[word].append((inton, mean))
			else:
				long_word_dic[word] = [(inton, mean)]
	return long_word_dic



def long_se(text):
	longest = 0
	tree = etree.parse(io.StringIO(text))
	sents = tree.xpath('//se/text()')
	for sent in sents:
		if re.search('[а-яА-Я]+', sent):
			pass
		else:
			if len(sent) > longest:
				ls = sent
				longest = len(sent)
	return ls



def sen_words(ls, chi_dic):
	words = []
	keys = chi_dic.keys()
	cut = ""
	mv = len(ls)
	n = len(ls)
	while n > 0:
		cut = ls[len(ls) - mv:]
		org = ls[len(ls) - mv:]
		i = len(cut)
		mv = 0
		while i > 0:
			if cut in keys:
				words.append(cut)
				i -= len(cut)
			else:
				mv += 1
				if mv == len(org):
				 	mv -= 1
				 	n -= 1
				 	words.append(cut)
				cut = cut[:-1]
				i -= 1
		n -= len(cut)
	print(words)
	return words



def write_xml(words, chi_dic):
	xml_dic = {}
	for word in words:
		if word in chi_dic.keys():
			xml_dic[word] = chi_dic[word]
	root = etree.Element('root')
	page = etree.SubElement(root, 'html')
	doc = etree.ElementTree(page)
	headElt = etree.SubElement(page, 'head')
	bodyElt = etree.SubElement(page, 'body')
	seElt = etree.SubElement(bodyElt, 'se')
	for word in words:
		if word in xml_dic.keys():
			wElt = etree.SubElement(seElt, 'w')
			wElt.text = word
			for v in xml_dic[word]:
				anaElt = etree.SubElement(wElt, 'ana', lex = word, transcri = v[0], sem = v[1])
		else:
			pElt = etree.SubElement(seElt, 'p')
			pElt.text = word
	xmlstr = minidom.parseString(etree.tostring(root)).toprettyxml(indent="   ")
	xmlstr = re.sub('<\/?p>', '', xmlstr)
	with open('china.xml', 'w', encoding = 'utf-8') as xml_doc:
		xml_doc.write(xmlstr)



#########################################################


with open('cedict_ts.u8', 'r', encoding = 'utf-8') as dic,\
open ('stal.xml', 'r', encoding = 'utf-8') as txt:
	dic = dic.read()
	text = txt.read()
chi_dic = make_dic(dic)
ls = long_se(text)
s_wds = sen_words(ls, chi_dic)
write_xml(s_wds, chi_dic)
