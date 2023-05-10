import psycopg2

connect = psycopg2.connect(
    database="CriticalPath",
    user="postgres",
    password="root",
    host="localhost",
    port="5432"
)

cur = connect.cursor()
peren = cur.execute('''CREATE TABLE Book4(
    UCH_OST_POL INTEGER,
    HAME_BEGIN CHAR(50))''')

connect.commit()
connect.close()
