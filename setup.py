"""

Name:Furkan T Goktas
Date: 9/25/2021
Assignment:#5 Role Based Access Control
Due Date: 9/26/2021
About this project: Develop code that encrypts data stored in a database for a small scale
                    using third-party Python libraries discussed in the course
All work below was performed by Furkan T Goktas

"""

import sqlite3

#create new db
conn = sqlite3.connect('CrapsDB.db')

# create Cursor to execute queries
cur = conn.cursor()


# drop table from database
try:
    conn.execute('''Drop table AGENTS''')
    # save changes
    conn.commit()
    print('Agent table dropped.')
except:
    print('Agent table did not exist')

# create table in database
cur.execute('''CREATE TABLE AGENTS(
Agent_ID INTEGER PRIMARY KEY NOT NULL,
AgentName TEXT NOT NULL,
Alias TEXT NOT NULL,
SecurityLevel INT NOT NULL,
Password TEXT NOT NULL);
''')

# save changes
conn.commit()
print('Agent Table created.')

"""
cur.execute('''Insert Into AGENTS ('Name','Alias','SecLvl','Password') 
Values ('Princess Diana', 28, 123,'test123');''')

conn.commit()

cur.execute('''Insert Into AGENTS ('Name','Alias','SecLvl','Password') 
Values ('Henry Thorgood', 56, 38,'test123');''')

conn.commit()

cur.execute('''Insert Into AGENTS ('Name','Alias','SecLvl','Password') 
Values ('Tina Fairchild', 38, 788,'test123');''')
"""
cur.executescript('''Insert Into AGENTS Values
                (1353, 'Princess Diana', 'Lady Di', 1, 'test123');

                Insert Into AGENTS Values
                (2032, 'Henry Thorgood', 'Goody 2 shoes', 3, 'test123');

                Insert Into AGENTS Values
                (3134, 'Tina Fairchild', 'Happy', 1, 'test123');

                Insert Into AGENTS Values
                (4034, 'Tom Smith', 'Sleepy', 1, 'test987');

                Insert Into AGENTS Values
                (5323, 'Kim Lovegood', 'Snoozy', 2, 'test987');

                Insert Into AGENTS Values
                (6362, 'Tim Harris', 'Doc', 3, 'test987');

                ''')

conn.commit()

# iterate over the rows
for row in cur.execute('SELECT * FROM AGENTS;'):
    print(row)


# close database connection
conn.close()
print('Connection closed.')
