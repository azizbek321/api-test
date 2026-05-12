from sqlite3 import connect

con = connect("../db.sqlite3")
cursor = con.cursor()

def Products():
    cursor.execute("select * from products")
    malumot = cursor.fetchall()
    return malumot