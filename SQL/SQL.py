import MySQLdb
import codecs
import csv




def imp_info():
    men = []
    women = []
    new_row = []
    run1 = False
    with open('vk.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter = ';', quotechar = '|')
        for row in csvreader:
            if run1 == True:
                try:
                    if row[3] == '1':
                        women.append(row)
                    else:
                        men.append(row)
                except IndexError:
                    pass
            else:
                run1 = True
    return (men, women)



def create(cursor):
    make_men = """CREATE TABLE KOGMEN(
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

    make_wom = """CREATE TABLE KOGWOM(
        Id INT,
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
    else:
        sex = 1    
    for row in vk_info[sex]:
        args = (row[0], row[1], row[2], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
        break
        if sex == 0:
            comm = "INSERT INTO KOGMEN (Id, First_name, \
                Last_name, City, Birthday, Home_town, \
                Relation, University, Graduation, Religion, Languages) \
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
        else:
            comm = "INSERT INTO KOGWOM (Id, First_name, \
                Last_name, City, Birthday, Home_town, \
                Relation, University, Graduation, Religion, Languages) \
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
        try:
            cursor.execute(comm, args)
            db.commit()
        except:
            db.rollback()

         

vk_info = imp_info()
db = MySQLdb.connect('localhost', 'guest1', 'n76Je4=wx6H', 'guest1_lyell', charset='utf-8')
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS KOGMEN")
cursor.execute("DROP TABLE IF EXISTS KOGWOM")
create(cursor)
insert('KOGMEN', db, vk_info, cursor)
insert('KOGWOM', db, vk_info, cursor)
db.close()