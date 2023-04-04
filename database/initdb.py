import sqlite3

db_file = 'database/dns.db'
if __name__ == '__main__':
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''CREATE TABLE xiaomiandns(domain TEXT PRIMARY KEY, ip TEXT, pubkey TEXT, nodetype TEXT,timestamp DATETIME)''')
        # node type contain 3 types: client, node, server
    except sqlite3.OperationalError:
        print("table xiaomiandns already exists")
    conn.commit()
    cursor.close()
    conn.close()
