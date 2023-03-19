import sqlite3

db_file = 'database/dns.db'
if __name__ == '__main__':
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    domain = 'mamahaha.wor12'
    ip = "1.1.1.11"
    pubkey = "asdfasdfadfsdf"
    cursor.execute("SELECT * FROM xiaomiandns WHERE domain = ? OR ip = ? OR pubkey = ?",
              (domain, ip, pubkey))
    existing_data = cursor.fetchall()
    if existing_data:
        print("qqqqqq")
    else:
        # Insert the new data
        cursor.execute(
            "INSERT INTO xiaomiandns (domain, ip, pubkey) VALUES (?, ?, ?)", (domain, ip, pubkey))
        print("Data inserted successfully")
        
    conn.commit()
    cursor.close()
    conn.close()
