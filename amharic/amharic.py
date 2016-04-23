import requests
from lxml import html, etree


def table():
	'''
	Grabs table from wikipedia and returns lists of list, where every frow from table is a list.

	arguments: none
	'''

	char_list = []
	site = requests.get("https://ru.wikipedia.org/wiki/Амхарский_язык")
	tree = html.fromstring(site.content)
	table = tree.xpath('//table[2]/tr//i/text() | //table[2]/tr//td/text() | //table[2]/tr//i/a/text()')
	i = 0 
	while i < 7:
		char_list.append(table[i:i+7])
		i += 7
	while i < len (table):
		char_list.append(table[i:i+8])
		i += 8
	return char_list


def conv_dic(char_list):
	'''
	Creates dictionary for converting amharic to coinciding phonetic alphabet characters.

	arguements: Char_list - Character list imported from table function.
	'''

	count_row = 0
	head_row = char_list[0]
	conv_dic = {}
	for row in char_list:
		count_col = 0
		if count_row != 0:
			for cell in row:
				if count_col == 0:
					char = cell
				else:
					vowel = head_row[count_col - 1]
					conv_dic.update({'{0}'.format(cell) : '{0}{1}'.format(char,vowel)})
				count_col += 1
		count_row += 1
	return conv_dic


def conv_text(conv_dic):
	'''
	Using dictionary converts amharic text into phonetic alphabet

	arguements: Conv_dic - Conversion dictionary from conv_dic function. Contains dictionary of amharic character keys with their coinciding phonetic alphabet values.
	'''
	temp_list = []
	fin_list = []
	with open('amharic.txt', 'r', encoding = 'utf8') as amdoc, \
	open('amharic_ipa.txt', 'w', encoding = 'utf8') as phondoc:
		amdoc = amdoc.read()
		for w in amdoc:
			for c in w:
				if c in conv_dic:
					c = conv_dic[c]
					temp_list.append(c)
				else:
					temp_list.append(c)
			temp_list = ''.join(temp_list)
			fin_list.append(temp_list)
			temp_list = []
		for word in fin_list:
			phondoc.write(word)



char_list = table()
conv_dic = conv_dic(char_list)
conv_text (conv_dic)