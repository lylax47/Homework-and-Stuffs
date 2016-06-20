import MySQLdb
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy())
ssh.connect('web-corpora.net', username='guest1', 
    password='c0rp7GG4_lkE3')



db = MySQLdb.connect('localhost', 'guest1', 'n76Je4=wx6H', 'guest1_lyell')
cursor = db.cursor()