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
    query = f"select id, date, date(date) as dd, hour(date) as hh, CAST(avg(moist_data) AS INTEGER) AS moist_data, cast(avg(temp_data) AS FLOAT ) as temp_data from data group by dd, hh;"


    try: 
        cur.execute(query)
    except mariadb.Error as e: 
        print(f"Error: {e}")

    # serialize results into JSON
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    print("allt")
    
    cur.close()
    conn.close()

    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))

    return json_data


def fetchLast():
        # connection for MariaDB
    try:
        conn = mariadb.connect(**legrow_config)
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # create a connection cursor
    cur = conn.cursor()
    # execute a SQL statement
    query = "SELECT * FROM data ORDER BY id DESC LIMIT 1;"

    print("last")
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