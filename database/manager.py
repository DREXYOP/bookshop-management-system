import mysql.connector

def connection():
    db = mysql.connector.connect(
        host='sql12.freemysqlhosting.net',
        user='sql12668515',
        password='a5NWN6g3dl',
        database='sql12668515',
    )
    return db