from sqlite3 import connect
words = ['Б', 'Л', 'Н', 'С', 'У']
dbConn = connect('dictionary.db')
cur = dbConn.cursor()
for word in words:
    cur.execute(f"""drop table if exists {word}""")
dbConn.commit()