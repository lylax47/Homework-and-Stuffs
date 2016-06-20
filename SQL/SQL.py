import MySQLdb
import codecs
import csv




def imp_info():
    men = []
    women = []
    new_row = []
    with codecs.open('vk.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter = ';', quotechar = '|')
        for row in csvreader:
            for x in row:
                new_row.append(x.decode('utf-8'))
            try:
                if row[3] == 1:
                    women.append(new_row)
                else:
                    men.append(new_row)
            except IndexError:
                pass
    return (men, women)



def create(cursor):
    make_men = """CREATE TABLE KOGMEN IF NOT EXISTS (
        Id INT,
        First_name  VARCHAR(50) NOT NULL,
        Last_name  VARCHAR(50),
        City  VARCHAR(50),  
        Birthday  VARCHAR(50),
        Home_town  VARCHAR(50),
        Relation  VARCHAR(50),
        University  VARCHAR(50),
        Graduation  VARCHAR(50),
        Religion  VARCHAR(50),
        Languages  VARCHAR(50))"""

    make_wom = """CREATE TABLE KOGWOM IF NOT EXISTS (
        ID INT,
        First_name  VARCHAR(50) NOT NULL,
        Last_name  VARCHAR(50),
        City  VARCHAR(50),  
        Birthday  VARCHAR(10),
        Home_town  VARCHAR(50),
        Relation VARCHAR(50),
        University  VARCHAR(50),
        Graduation  VARCHAR(50),
        Religion  VARCHAR(50),
        Languages  VARCHAR(50))"""
    cursor.execute(make_men)
    cursor.execute(make_wom)   



def insert(table, db, vk_info, cursor):
    if table == 'KOGMEN':
        sex = 0
        comm = "INSERT INTO KOGMEN (ID, FIRST_NAME, \
                LAST_NAME, CITY, BIRTHDAY, HOME_TOWN, \
                RELATION, UNIVRSITY, GRADUATION, RELIGION, LANGUAGES) \
                VALUES ('%d', %s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                (row[0], row[1], row[2], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
    else:
        sex = 1
        comm = "INSERT INTO KOGWOM (ID, FIRST_NAME, \
                LAST_NAME, CITY, BIRTHDAY, HOME_TOWN, \
                RELATION, UNIVRSITY, GRADUATION, RELIGION, LANGUAGES) \
                VALUES ('%d', %s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                (table, row[0], row[1], row[2], row[4], row[5], row[6], row[7], row[8], row[9], row[10])        
    for row in vk_info[sex]:
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