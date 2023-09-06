import pymysql
import configparser

# establish connection with mysql local
parser = configparser.ConfigParser()
parser.read("pipeline.conf")
hostname = parser.get("mysql_config", "hostname")
port = parser.get("mysql_config", "port")
username = parser.get("mysql_config", "username")
dbname = parser.get("mysql_config", "database")
password = parser.get("mysql_config", "password")

conn = pymysql.connect(host=hostname,
        user=username,
        password=password,
        db=dbname,
        port=int(port))

query = """SELECT COALESCE(MAX(LastUpdated),
        '1900-01-01')
        FROM Orders;"""

cursor = conn.cursor()
cursor.execute(query)
result = cursor.fetchone()

# there's only one row and column returned
last_updated_warehouse = result[0]
print(last_updated_warehouse)

m_query = """SELECT *
    FROM Orders
    WHERE LastUpdated > %s;"""
local_filename = "order_extract.csv"

cursor = conn.cursor()
cursor.execute(m_query, (last_updated_warehouse,))
results = cursor.fetchall()

cursor.close()
conn.close()

print(results)