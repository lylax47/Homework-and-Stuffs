templ = "The elderly passenger sitting on the north-window side of that inexorably moving railway coach, next to an empty seat and facing two empty ones, \
was none other than Professor Timofey Pnin.Ideally bald, sun-tanned, and clean-shaven, he began rather impressively with that great brown dome of his, \
tortoise-shell glasses (masking an infantile absence of eyebrows), apish upper lip, thick neck, and strong-man torso in a tightish tweed coat, but ended, \
somewhat disappointingly, in a pair of spindly legs (now flannelled and crossed) and frail-looking, almost feminine feet.When inviting him to deliver a Friday-evening lecture at Cremona ,\
some two hundred versts west of Waindell, Pnin's academic perch since 1945 ,  the vice-president of the Cremona Women's Club, a Miss Judith Clyde, \
had advised our friend that the most convenient train left Waindell at 1.52 p.m., reaching Cremona at 4.17; but Pnin ,  who, like so many Russians, was inordinately \
fond of    everything in the line of timetables, maps, catalogues, collected them, helped himself freely to them with the bracing pleasure of getting something for nothing, \
and took especial pride in puzzling out schedules for himself ,  had discovered, after some study, an inconspicuous reference mark against a still more convenient train \
(Lv. Waindell 2.19 p.m., Ar. Cremona 4.32 p.m.); the mark indicated that Fridays, and Fridays only, the two-nineteen stopped at Cremona on its way to a distant and \
much larger city, graced likewise with a mellow Italian name.Unfortunately for Pnin, his timetable was five years old and in part obsolete."
samp = ['The elderly passenger sitting on the ЖПП north-window side 6рнthat inexorably moving railway coach, next to an empty seat and facing two empty ones, \
was none other than Professor Timofey Pnin.', 'Ideally baldбдмаб sun-tanned, and clean-shaven, he began rather ejnfjernf8585hg impressively with that great brown dome of his, \
tortoise-shell glasses (masking an infantile absence of eyebrows), apish upper lip, thick neck, and strong-man torso in a tightish tweed coat, but ended, \
somewhat disappointingly, in a pair of spindly legs (now flannelled and crossed) and frail-looking, almost vnd  oo eeov finine feet.', "When inviting him to deliver \
a Friday-evening lecture at Cremona вЂ” some two hundred versts west of Waindell, Pnin's academic perch since 1945 вЂ” the vice-president of the Cremona Women's Club, \
a Miss Judith Clyde, had advised our friend that the most convenient train left Waindell at 1.52 p.m., reaching Cremona at 4.17; but Pnin вЂ” who, like so many Russians,\
was inordinately fond of everything in the line of timetables, maps, catalogues, collected them, helped himself freely to them with the bracing pleasure of getting something \
for nothing, and took especial pride in puzzling out schedules for himself вЂ” had discovered, after some study, an inconspicuous reference mark against a still more \
convenient train (Lv. Waindell 2.19 p.m., Ar. Cremona 4.32 p.m.); the mark indicated that Fridays, and Fridays only, the two-nineteen stopped at Cremona on its way to a \
distant and much larger city, graced likewise with a mellow Italian name.", "Unfortunately for Pnin, his timetable was five years old and in part obsolete."]



i1 = 0
i2 = 0
si = 0
length1 = len(templ)
while i1 <= length1 - 1:
	sent = samp[si]
	length2 = len(sent)
	last_char = sent[length2 - 1]
	sent_list = []
	while i2 <= (length2 - 1):
		try:
			sent_list.append(templ[i1])
			i2 += 1
			i1 += 1
		except IndexError:
			break
	new_sent = ''.join(sent_list)
	if new_sent[i2 - 1] == last_char:
		samp[si] = new_sent
	else:
		i3 = 0
		third = (i2/3)
		while (new_sent[i2 - 1] != last_char) and i3 < third :
			i2 -= 1
			i3 += 1
		# if i3 == third:
		# 	i2 += third
		# 	i4 = i1
		# 	while (templ[i1] != last_char) and i3 >= 0:
		# 		i1 += 1
		# 	new_sent = new_sent + templ[i4:i1]
		else:
			new_sent = new_sent[:i2]
			i1 -= (length2 - i2)
		samp[si] = new_sent
	si += 1
	i2 = 0
print(samp)


