import mysql.connector, sys, random

host_name = '198.251.89.164'  # or your PostgreSQL server's IP address
port_number = 3306  # default PostgreSQL port
database_name = 'mrmetalg_test'  # name of your database
database_user = 'mrmetalg_test'  # your PostgreSQL username
database_password = 'ThePassword69!'  # your PostgreSQL password

def establish_db_connection():
     return mysql.connector.connect(
        host=host_name,
        user=database_user,
        password=database_password,
        database=database_name
     )


print(f"Commencing database test 1......")

test_limit = 200


test_user = 'dummyuser'
test_password = 'dummypassword'


