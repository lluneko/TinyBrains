import sqlite3

db_file = '../db/users_base.sqlite'
con = sqlite3.connect(db_file)
cur = con.cursor()
res = cur.execute(f"SELECT history FROM users WHERE name = 'ol'").fetchall()
print(res[0][0])

