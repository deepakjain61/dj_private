import sqlite3

conn = sqlite3.connect('user.db')
"""
print "Opened database successfully";
conn.execute('''CREATE TABLE user_info
       (id INTEGER PRIMARY KEY  AUTOINCREMENT,
       user_name  TEXT    NOT NULL,
       age  INT,
       country   CHAR(50),
       email_id TEXT,
       phone_no TEXT,
       password TEXT);''')

print "Table created successfully";
"""
conn.execute('''INSERT INTO user_info (user_name,age,country,email_id,phone_no,password)
VALUES ( 'Paul', 32, 'California', 'deepakjain61@gmail.com','7768981551', '123' );''')
conn.commit()
for row in conn.execute('SELECT * FROM user_info'):
    print row
print "main hun hero ...tera"
conn.close()
