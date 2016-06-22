import xlrd
import json
import re


def break_text(data):
	'''
	Breaks up large texts into smaller chunks based on their sizes.

	input - data: Imported excel info.

	output - new_rows: List of excel table rows with additional rows for broken-up texts.
	'''

	new_rows = []
	run1 = False
	for row in data:
		if run1 == True:
			if row[-2] != 'none':
				word_c = int(row[-2])
				if word_c > 100000:
					i = 1
					while i <= 3:
						row[-2] = (word_c/3)
						row[0] = (row[0] + '{0}'.format(i))
						new_rows.append(row)
						i += 1
				elif 80000 < word_c < 100000:
					i = 1
					while i <= 2:
						row[-2] = (word_c/2)
						row[0] = (row[0] + '{0}'.format(i))
						new_rows.append(row)
						i += 1
				else:
					new_rows.append(row)
		else:
			run1 = True
	return new_rows



def cats(new_rows):
	'''
	Rewrites simplified genre values into sphere column to better organize texts.

	input - new_rows: List of rows exported from break_text function.

	output - cat_row: List of rows with altered sphere column values.
	'''

	cat_rows = []
	for row in new_rows:
		if re.match('художественная(.*)', row[6]):
			row[6]= 'художественная'
		elif re.match('официально-деловая(.*)', row[6]):
			row[6]= 'официально-деловая'
		elif re.match('производственно-техническая(.*)', row[6]):
			row[6]= 'производственно-техническая'
		elif re.match('реклама(.*)', row[6]):
			row[6]= 'реклама'
		elif re.match('публицистика(.*)', row[6]):
			row[6]= 'публицистика'
		elif re.match('учебно-научная(.*)', row[6]):
			row[6]= 'учебно-научная'
		elif re.match('[бытовая|электронная коммуникация](.*)|', row[6]):
			row[6]= 'бытовая'
		elif re.match('церковно-богословская(.*)', row[6]):
			row[6]= 'церковно-богословская'
		cat_rows.append(row)
	return cat_rows



def years(cat_rows):
	'''
	Places rows into dictionary based upon their year of creation. (Uses first date value given in the case time given is a span)

	input - cat_rows: List of rows exported from cats function.

	output - year_rows:  Dictionary of excel spreadsheet rows organized by date of creation.
	'''

	year_rows = {1950:[], 1961:[], 1971:[], 1981:[], 1991:[], 2001:[], 2011:[]}
	for row in cat_rows:
		num = str(row[5])
		if re.match('(195[0-9])(.*)', num) is not None:
			year_rows[1950].append(row)
		elif re.match('(196[1-9])(.*)', num) is not None:
			year_rows[1961].append(row)
		elif re.match('(197[1-9])(.*)', num) is not None:
			year_rows[1971].append(row)
		elif re.match('(198[1-9])(.*)', num) is not None:
			year_rows[1981].append(row)
		elif re.match('(199[1-9])(.*)', num) is not None:
			year_rows[1991].append(row)
		elif re.match('(200[1-9])(.*)', num) is not None:
			year_rows[2001].append(row)
		elif re.match('(201[1-9])(.*)', num) is not None:
			year_rows[2011].append(row)
	return year_rows

def equal (year_rows):
	'''
	Equalize amount of text from given genres and dates by appending to last_list
	a text with a combination of the lowest date and genre word count values.

	input - year_rows: Dictionary exported from years function.

	output - last_list: list with finalized rows, ready for printig to csv.
	'''

	total_wc = 100000000
	cat_d = {'xud_wc':0, 'off_wc':0, 'pro_wc':0, 'rek_wc':0, 'pub_wc':0, 'uch_wc':0, 'bit_wc':0, 'serk_wc':0}
	year_d = {'1950_wc':0, '1961_wc':0, '1971_wc':0, '1981_wc':0 , '1991_wc':0, '2001_wc':0, '2011_wc':0}
	while total_wc > 0:
		for row in cat_rows:
			y = 0
			c = 0
			cat_l = [year_d['xud_wc'], year_d['off_wc'], year_d['pro_wc'], year_d['rek_wc'], \
			year_d['pub_wc'], year_d['uch_wc'], year_d['bit_wc'], year_d['serk_wc']] 
			year_l = [year_d['1950_wc'], year_d['1961_wc'], year_d['1971_wc'], year_d['1981_wc'], \
			year_d['1991_wc'], year_d['2001_wc'], year_d['2011_wc']]
			c_sort = cat_l.sort()
			y_sort = year_l.sort()
			c_val = c_sort[0]
			y_val = y_sort[0]

### Unfortunately I do not currently have time to finish becasue of other finals.
### I should also note that this was not completed during the exam period, so grade as you wish.
### The problem was that I had never worked with excel files before and was previously unfamiliar 
### with how to open and work with them.
### Everything should function up until the function equal.
### Further I would have written a function for writting the organized data to csv.

				






wb = xlrd.open_workbook('source_post1950_wordcount.xls')
s = wb.sheet_by_index(0)
data = [[s.cell_value(r, c) for c in range (s.ncols)] for r in range(s.nrows)]
new_rows = break_text(data)
cat_rows = cats(new_rows)
year_rows = years(cat_rows)
print(year_rows[1950][0])
