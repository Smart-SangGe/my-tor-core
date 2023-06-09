import sqlite3
import argparse

# 用于创建
db_file = 'database/dns.db'
if __name__ == '__main__':
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    parser = argparse.ArgumentParser()
    parser.add_argument('--add', action='store_true', help='add test data')
    args = parser.parse_args()
    try:
        cursor.execute(
            '''CREATE TABLE xiaomiandns(domain TEXT PRIMARY KEY, ip TEXT,timestamp DATETIME)''')
    except sqlite3.OperationalError:
        print("table xiaomiandns already exists")
    conn.commit()
    if args.add:
    
        test_data = [
        ('example.xiaomian', '192.168.1.1'),
        ('google.xiaomian', '8.8.8.8'),
        ('yahoo.xiaomian', '98.138.219.231')
        ]

        for data in test_data:
            domain, ip = data
            cursor.execute("INSERT INTO xiaomiandns (domain, ip, timestamp) VALUES (?, ?, DATETIME('now'))", (domain, ip))

    # 提交更改到数据库
    conn.commit()
    cursor.close()
    conn.close()
