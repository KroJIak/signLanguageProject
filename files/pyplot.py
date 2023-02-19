import matplotlib.pyplot as plt
from sqlite3 import connect

nameWord = 'А'
dbConn = connect('../dictionary.db')
cur = dbConn.cursor()
cur.execute(f"""SELECT * FROM {nameWord};""")
word = cur.fetchall()
dbConn.commit()

fig =plt.figure(figsize=(7, 7))
ax = fig.add_subplot(projection='3d')

sequence_containing_x_vals = [0] * 21
sequence_containing_y_vals = list(map(lambda x: x[1], word))
sequence_containing_z_vals = list(map(lambda x: x[0], word))

ax.scatter(sequence_containing_x_vals, sequence_containing_y_vals, sequence_containing_z_vals)
plt.show()