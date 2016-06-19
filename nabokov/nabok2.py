import re
import os
from lxml import etree



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
		sent1 = list(str(templ[si1]))
		sent2 = list(str(samp[si2]))
		ci1 = 0
		ci2 = 0
		sl1 = len(sent1[ci1:])
		sl2 = len(sent2[ci2:])
		er = 0
		if sl1 > sl2:
			while ci2 <= (sl2 - 1):
				char1 = sent1[ci1]
				char2 = sent2[ci2]
				if char1 == char2:
					ci1 += 1
					ci2 += 1
				else:
					sent2[ci2] = char1
					er += 1
					ci1 += 1
					ci2 += 1
			if sl1 - sl2 - er == 0:
				new_sent = ''.join(sent2[:(sl2 - er - 1)])
			else:
				while char2 not in [".'?!"]:
					ci2 -= 1
					char2 = sent2[ci2]
				new_sent = sent2[:ci2]
				new_samp.append(new_sent)
				nsl = len(new_sent)
				si2 += 1
				new_sent = ''.join(sent1[(nsl - 1):])
		elif sl1 < sl2:
			while ci1 <= (sl1 - 1):
				char1 = sent1[ci1]
				char2 = sent2[ci2]
				if char1 == char2:
					ci1 += 1
					ci2 += 1
				else:
					sent2[ci2] = char1
					er += 1
					ci1 += 1
					ci2 += 1
			if sl2 - sl1 - er == 0:
				new_sent = ''.join(sent2[:(sl2 - er - 1)])
			else:
				print(sent1)
				print(sent2)
				while char2 not in [".'?!"]:
					ci2 += 1
					char2 = sent2[ci2]
				new_sent = ''.join(sent2[:ci2])
				si2 += 1
				ci2 = 0
				break
		else:
			while ci1 <= (sl1 - 1):
				char1 = sent1[ci1]
				char2 = sent2[ci2]
				if char1 == char2:
					ci1 += 1
					ci2 += 1
				else:
					sent2[ci2] = char1
					er += 1
					ci1 += 1
					ci2 += 1
			new_sent = ''.join(sent2)
		si1 += 1
		si2 += 2
		print(new_sent)
		new_samp.append(new_sent)
		print(new_samp)




#def xml_write():



tree = etree.parse('pnin_barabtarlo.xml')
orig_sents = tree.xpath('//se[@lang = "en"]/text()')
iljin = comp("iljin")
nosik = comp("nosik")
iljin_ru = rus_comp('iljin')
nosik_ru = rus_comp('nosik')
#nosik_new = rep(orig_sents, nosik)
iljin_new = rep(orig_sents, iljin)