import sqlite3
from faker import Faker
import sqlite3


NUMBER_OF_RECORDS = 1_000_000

con = sqlite3.connect('users.db');
cur = con.cursor()

def create_table(con :sqlite3.Connection):
    con.execute('''CREATE TABLE users
               (id INTEGER PRIMARY KEY, first_name VARCHAR, last_name VARCHAR, email VARCHAR);''')
    index_ids = ("CREATE INDEX ix_users_id ON users(id);")
    index_email = ("CREATE INDEX ix_users_email ON users(email);")
    con.execute(index_ids)
    con.execute(index_email)

def quickId(x, y):
    return x*1_000_00+y

def generate_x_records(con:sqlite3.Connection, count: int, fake = Faker()):
    batch_size = 1_000_00
    for i in range(int(count/batch_size)):
        current_batch = []
        for j in range(batch_size):
            id = quickId(i, j)            
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name}{last_name}@fakeemail.com"
            current_batch.append((id, first_name, last_name, email))
        con.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", current_batch)
        # cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (i, first_name, last_name, email))
    con.commit()



def drop_table(con: sqlite3.Connection):
    con.execute('DROP TABLE users')

def main():
    con = sqlite3.connect('users.db', isolation_level=None)    
    con.execute('PRAGMA journal_mode = OFF;')
    con.execute('PRAGMA synchronous = 0;')
    con.execute('PRAGMA cache_size = 1000000;')  
    con.execute('PRAGMA locking_mode = EXCLUSIVE;')
    con.execute('PRAGMA temp_store = MEMORY;')
    # drop_table(con)
    # create_table(con)
    generate_x_records(con, NUMBER_OF_RECORDS)


if __name__ == '__main__':
    main()