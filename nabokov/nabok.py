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
	length1 = len(templ)
	while si1 <= len(templ) - 1:
		if templ[si1] == samp[si2]:
			new_samp.append(templ[si1])
		elif len(templ[si1]) > len(samp[si2]) + 10:
			tup = ordering(templ, samp, si1, si2)
			si1 = tup[0]
			si2 = tup[1]
			new_samp.append(tup[2])
		elif len(samp[si2]) > len(templ[si1]) + 10:
			tup = ordering(samp, templ, si2, si1)
			si1 = tup[1]
			si2 = tup[0]
			new_samp.append(tup[2])
		else:
			new_samp.append(templ[si1])
		si1 += 1
		si2 += 1


def ordering(big, little, big_i, lit_i):
	sent = little[lit_i]
	test = little[lit_i]
	prev_sen = little[(lit_i - 1)]
	i1 = 0
	orig_sen = big[big_i]
	if prev_sen[len(prev_sen) - 2: len(prev_sen) - 1] != orig_sen[len(orig_sen) - 2: len(orig_sen) - 1]:
		while sent[len(sent) - 2: len(sent) - 1] != orig_sen[len(orig_sen) - 2: len(orig_sen) - 1]:
			lit_i += 1
			i1 += 1
			try:
				sent = little[lit_i]
			except IndexError:
				print(test)
				print(prev_sen)
				print(orig_sen)
				print(big_i)
				print(lit_i)
				break
		si3 = lit_i
		while i1 >= 0:
			# try:
			sent = little[si3]
			# except IndexError:
			# 	print(test)
			# 	print(prev_sen)
			# 	print(orig_sen)
			# 	print(big_i)
			# 	print(lit_i)
			beg = sent[0:1]
			end = sent[len(sent) -4: len(sent) - 2]
			if ')' in end:
				exp = re.search('(({0}(.*))'.format(beg), orig_sen)
			else:
				exp = re.search('({0}(.*))'.format(beg), orig_sen[0:len(orig_sen)-1])
			try:
				cut = exp.group(1)
			except AttributeError:
				print(test)
				print(prev_sen)
				print(orig_sen)
				print(big_i)
				print(lit_i)
				break
			si3 -= 1
			i1 -= 1
	else:
		cut = big[big_i]
	try:
		return (big_i, lit_i, cut)
	except UnboundLocalError:
		print(orig_sen)
		print(test)
		





#def xml_write():



tree = etree.parse('pnin_barabtarlo.xml')
orig_sents = tree.xpath('//se[@lang = "en"]/text()')
iljin = comp("iljin")
nosik = comp("nosik")
iljin_ru = rus_comp('iljin')
nosik_ru = rus_comp('nosik')
#nosik_new = rep(orig_sents, nosik)
iljin_new = rep(orig_sents, iljin)




#first attempt. (I don't think it'll work)

# def rep(templ, samp):
# 	i1 = 0
# 	i2 = 0
# 	si = 0
# 	length1 = len(templ)
# 	while i1 <= length1 - 1:
# 		try:
# 			sent = samp[si]
# 			length2 = len(sent)
# 			last_char = sent[length2 - 1]
# 			sent_list = []
# 			while i2 <= (length2 - 1):
# 				try:
# 					sent_list.append(templ[i1])
# 					i2 += 1
# 					i1 += 1
# 				except IndexError:
# 					break
# 			new_sent = ''.join(sent_list)
# 			if new_sent[i2 - 1] == last_char:
# 				samp[si] = new_sent
# 			else:
# 				i3 = 0
# 				third = (i2/3)
# 				while (new_sent[i2 - 1] != last_char) and i3 < third :
# 					i2 -= 1
# 					i3 += 1
# 				if i3 == third:
# 					i2 += third
# 					i4 = i1
# 					while (templ[i1] != last_char) and i3 >= 0:
# 						i1 += 1
# 					new_sent = new_sent + templ[i4:i1]
# 				else:
# 					new_sent = new_sent[:i2]
# 					i1 -= (length2 - i2)
# 				samp[si] = new_sent
# 			si += 1
# 			i2 = 0
# 		except IndexError:
# 			print(si)
# 			for sent in samp:
# 				with open('test.txt', 'a', encoding='utf-8') as test:
# 					test.write(sent + '\n')
# 			break
# 	return samp