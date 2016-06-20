import MySQLdb
import codecs
import csv




def imp_info():
    men = []
    women = []
    with codecs.open('vk.csv', 'r', encoding = 'utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter = ';', quotechar = '|')
        for row in csvreader:
            print row
            try:
                if row[3] == 1:
                    women.append(row)
                else:
                    men.append(row)
            except IndexError:
                print row
                break
    return (men, women)



def create(cursor):
    make_men = """CREATE TABLE KOGMEN (
        ID INT
        FIRST_NAME  CHAR(50) NOT NULL,
        LAST_NAME  CHAR(50),
        CITY CHAR(50),  
        BIRTHDAY CHAR(10),
        HOME_TOWN CHAR(50)
        RELATION CHAR(50)
        UNIVERSITY CHAR(50)
        GRADUATION CHAR(50)
        RELIGION CHAR(50)
        LANGUAGES CHAR(50))"""

    make_wom = """CREATE TABLE KOGWOM (
        ID INT
        FIRST_NAME  CHAR(50) NOT NULL,
        LAST_NAME  CHAR(50),
        CITY CHAR(50),  
        BIRTHDAY CHAR(10),
        HOME_TOWN CHAR(50)
        RELATION CHAR(50)
        UNIVERSITY CHAR(50)
        GRADUATION CHAR(50)
        RELIGION CHAR(50)
        LANGUAGES CHAR(50))"""
    cursor.execute(make_men)
    cursor.execute(make_wom)   



def insert(table, db, vk_info, cursor):
    if table == 'KOGMEN':
        sex = 0
    else:
        sex = 1
    for row in vk_info[sex]:
        comm = "INSERT INTO '%s' (ID, FIRST_NAME, \
               LAST_NAME, CITY, BIRTHDAY, HOME_TOWN, \
               RELATION, UNIVRSITY, GRADUATION, RELIGION, LANGUAGES) \
               VALUES ('%d', %s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
               (table, row[0], row[1], row[2], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

         

vk_info = imp_info()
db = MySQLdb.connect('localhost', 'guest1', 'n76Je4=wx6H', 'guest1_lyell')
cursor = db.cursor()
create(cursor)
insert('KOGMEN', db, vk_info, cursor)
insert('KOGWOM', db, vk_info, cursor)