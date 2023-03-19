import sqlite3

db_file = 'dns.db'
if __name__ == '__main__':
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute('''CREATE TABLE xiaomiandns(domain TEXT PRIMARY KEY, ip TEXT, pubkey TEXT)''')
    except sqlite3.OperationalError:
        print("table xiaomiandns already exists")
    conn.commit()
    cursor.close()
    conn.close()