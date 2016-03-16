ipa = {"ბ":"b", "დ":"d", "ძ":"dz", "ჯ":"dʒ", "გ":"ɡ", "ღ":"ɣ", "ჰ":"h", "კ":"kʼ", "ქ":"kʰ", "ლ":"l", "მ":"m", "ნ":"n", "პ":"pʼ", "ფ":"pʰ", "ყ":"qʼ", "რ":"r", "ს":"s", 
"შ":"ʃ", "ტ":"tʼ", "თ":"tʰ", "წ":"tsʼ", "ც":"tsʰ", "ჭ":"tʃʼ", "ჩ":"tʃʰ", "ვ":"v", "ხ":"x", "ზ":"z", "ჟ":"ʒ", "ა":"ɑ", "ე":"ɛ", "ი":"i", "ო":"ɔ", "უ":"u"}   #Dictionary containing coresponding Georgian and IPA characters.
ipa_list = []   # Final list that will be written to fo destination.
temp_ipa = []   # Temporary placeholder for words, while characters are converted. This way spaces and punctuation are saved (original formating).

f = open('C:\\Users\\John\\Desktop\\py_files\\питон\\Georgian_text.txt', 'r', encoding = 'utf-8-sig')
fo = open('C:\\Users\\John\\Desktop\\py_files\\питон\\Georgian_text_ipa.txt', 'w', encoding = 'utf-8-sig') #Change directories and file names as needed. 
text = f.read()
text_words = text.split()
for w in text_words:
    for c in w:
        if c in ipa:
            c = ipa[c]
            temp_ipa.append(c)  #Converts Georgian letter then appends to temp list.
        else:
            temp_ipa.append(c)  #Appends non-Georgian characters to temp list.
    temp_ipa = "".join(temp_ipa)#Joins converted charcters.
    ipa_list.append(temp_ipa)   #Appends converted word to final list.
    temp_ipa = []               #Clears temp list for reuse in for loop.
for word in ipa_list:
    fo.write(word + " ")
f.close()
fo.close()