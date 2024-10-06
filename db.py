import psycopg2

DB_NAME = "Hackathon.sqlite"
credentials = {
    'user': "django",
    'host': "192.168.243.130",
    'database': "zelf_team_chicken_db",
    'password': "django",
    'port': 5432
}

def execute_query(sql_query):
    conn = psycopg2.connect(**credentials)
    cur = conn.cursor()
    cur.execute(sql_query)
    conn.commit()
    conn.close()

# def is_table_exist(table_name):
#     sql_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
#     conn = sqlite3.connect(DB_NAME)
#     cur = conn.cursor()
#     response = cur.execute(sql_query).fetchall()
#     return True if len(response) > 0 else False


def insert_data(table_name, all_info):
    print("Calling DB ---")
    conn = psycopg2.connect(**credentials)
    cur = conn.cursor()
    column_name = all_info[0].keys()
    columns = ",".join(column_name)
    print(columns)
    value_string = ""
    for i in range(len(column_name)):
        if i < len(column_name) - 1:
            value_string = value_string+"%s, "
        else:
            value_string = value_string+"%s"

    sql_query = f'''INSERT INTO {table_name} ({columns}) values ({value_string})'''
    print(sql_query)
    for info in all_info:
        values = info.values()
        print(values)
        cur.execute(sql_query, [ value for value in values])
        conn.commit()
    conn.close()
