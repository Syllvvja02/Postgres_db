from psycopg2 import connect, OperationalError, sql, DatabaseError

try:
    cnx = connect(
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432,
        database='postgres'
    )

    cursor = cnx.cursor()
    print("Connected!")

except OperationalError as error:
    print("Connection error!")
    raise ValueError(f'Connection error: {error}')

query_create_table_user = sql.SQL("""
CREATE TABLE IF NOT EXISTS{table_name} (
id SERIAL,
name VARCHAR(50),
email VARCHAR(50) UNIQUE,
password VARCHAR(50) DEFAULT 'ALA',
PRIMARY KEY (id)
)
""").format(table_name=sql.Identifier('User'))

query_create_table = sql.SQL("""
CREATE TABLE IF NOT EXISTS{table_name} (
id SERIAL PRIMARY KEY,
serial VARCHAR(85),
city VARCHAR(188),
notes text,
user_id SMALLINT,
FOREIGN KEY (user_id) REFERENCES {table_name_foreign}(id)
)
""").format(
    table_name=sql.Identifier('Adress'),
    table_name_foreign=sql.Identifier('User')
)

query_create_values = sql.SQL("""
INSERT INTO {table_name} (name, email, password)
VALUES (%s, %s, %s)
""").format(table_name=sql.Identifier('User'))

query_detele_values = sql.SQL("""
DELETE FROM {table_name} WHERE id=%s
""").format(table_name=sql.Identifier('User'))

query_update = sql.SQL("""
UPDATE {table_name} SET email=%s WHERE id=%s
""").format(table_name=sql.Identifier('User'))

query_alter = sql.SQL("""ALTER TABLE {table_name} ADD COLUMN price DECIMAL(7,2) DEFAULT 0""").format(
    table_name=sql.Identifier('User'))
query_alter2 = sql.SQL(
    """ALTER TABLE {table_name} ADD COLUMN date_of_created TIMESTAMP DEFAULT
     CURRENT_TIMESTAMP""").format(
    table_name=sql.Identifier('Address'))

try:
    with cnx:
        try:
            cursor.execute(query_create_table)
        except DatabaseError as error:
            print(error)

        # try:
        #     cursor.execute(query_create_values, ('Ala', 'Ma@piesa', 'mruczek'))
        # except DatabaseError as error:
        #     print(f'{error}')
        # try:
        #     cursor.execute(query_detele_values, (1,))
        # except DatabaseError as error:
        #     print(f'{error}')

        try:
            cursor.execute(query_update, ("mikos@wp.pl", 2))
        except DatabaseError as error:
            print(f'{error}')


# except ValueError:
#     pass
# else:
#     pass
finally:
    cnx.close()