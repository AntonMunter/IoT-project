import mariadb
import sys
import os

legrowConfig = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('MYSQL_ROOT_PASSWORD'),
    'database': os.getenv('LG_DATABASE')
}

def insert(moist_data, temp_data):
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(**legrowConfig)
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    cur = conn.cursor()
    query = f"INSERT INTO data (moist_data, temp_data) VALUES ({moist_data}, {temp_data})"
    try: 
        cur.execute(query) 
        conn.commit()
    except mariadb.Error as e: 
        print(f"Error: {e}")
    
    conn.close()
