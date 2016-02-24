import os, json, dicttoxml
from pymystem3 import Mystem

m = Mystem()
top = 'C:\\Users\\John\\Desktop\\py_files\\питон\\korpus\\no_marks'
for root, dirs, files in os.walk(top):
    for name in files:
        loc = os.path.join(root, name)
        loc_list = loc.split('\\')  #creates list in order to remove path content
        new_root = loc.replace('\\no_marks\\{0}\\{1}\\{2}'.format(loc_list[8], loc_list[9], loc_list[10]), '') #removes path ending
        dir_marks = os.path.join(new_root + '\\marks\\{0}\\{1}'.format(loc_list[8], loc_list[9]))   #adds new path ending for json.docs
        dir_xml = os.path.join(new_root + '\\xml\\{0}\\{1}'.format(loc_list[8], loc_list[9]))       #adds new path ending for xml docs
        new_name = name.replace('.txt', '')
        if not os.path.exists(dir_marks):   #makes nesessary dirs if not present
            os.makedirs(dir_marks)
        if not os.path.exists(dir_xml):
            os.makedirs(dir_xml)
        with open(loc, "r", encoding = 'utf-8') as doc:
            text_doc = doc.read()
            lines = doc.readlines()
            info = json.dumps(m.analyze(text_doc), ensure_ascii = False)  #creates text file with gram and lem info
        with open("{0}\\{1}.json".format(dir_marks, new_name), 'w', encoding = 'utf-8') as doc_marks:
            doc_marks.write(info)
        xml = dicttoxml.dicttoxml(info).decode('utf-8')     #converts json to xml
        with open("{0}\\{1}.xml".format(dir_xml, new_name), 'w', encoding = 'utf-8') as doc_xml:
            doc_xml.write(xml)


