import sqlite3

DB_NAME = "Hackathon.sqlite"

def execute_query(sql_query):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(sql_query)
    conn.commit()
    conn.close()

def is_table_exist(table_name):
    sql_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    response = cur.execute(sql_query).fetchall()
    return True if len(response) > 0 else False


def insert_data(table_name, all_info):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    column_name = all_info[0].keys()
    columns = ",".join(column_name)
    value_string = ""
    for i in range(len(column_name)):
        if i < len(column_name) - 1:
            value_string = value_string+"?, "
        else:
            value_string = value_string+"?"

    sql_query = f'''INSERT INTO {table_name} ({columns}) values ({value_string})'''
    print(sql_query)
    for info in all_info:
        values = info.values()
        print(values)
        cur.execute(sql_query, [str(value).encode('utf-8', 'ignore').decode('utf-8', 'ignore') for value in values])
        conn.commit()
    conn.close()
