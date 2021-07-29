import mariadb
import sys
import os
import json


legrow_config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('MYSQL_ROOT_PASSWORD'),
    'database': os.getenv('LG_DATABASE')
}


def fetchData(size):
        # connection for MariaDB
    try:
        conn = mariadb.connect(**legrow_config)
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # create a connection cursor
    cur = conn.cursor()
    # execute a SQL statement
    query = f"select * from data ORDER BY id DESC LIMIT {size}"

    try: 
        cur.execute(query) 
    except mariadb.Error as e: 
        print(f"Error: {e}")

    # serialize results into JSON
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    
    cur.close()
    conn.close()

    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    return json_data