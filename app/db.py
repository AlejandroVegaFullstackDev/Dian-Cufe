# db.py
import pymysql.cursors

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='dian_facturas',
    cursorclass=pymysql.cursors.DictCursor
)
