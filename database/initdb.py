import sqlite3

# 用于创建
db_file = 'database/dns.db'
if __name__ == '__main__':
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''CREATE TABLE xiaomiandns(domain TEXT PRIMARY KEY, ip TEXT,timestamp DATETIME)''')
    except sqlite3.OperationalError:
        print("table xiaomiandns already exists")
    conn.commit()
    cursor.close()
    conn.close()
