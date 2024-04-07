from repositories.db import get_pool
from psycopg.rows import dict_row
        

def login(username, password) -> list[dict[str, any]]:
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        SELECT * FROM users
                        WHERE username = %s AND password = %s
                        ''', (username, password, ))
            rows = cur.fetchall()
            return rows

def checkIFUserExists(username) -> list[dict[str, any]]:
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        SELECT * FROM users
                        WHERE username = %s
                        ''', (username, ))
            rows = cur.fetchall()
            return rows

def SignUp(username, password, firstname, lastname) -> list[dict[str, any]]:
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        
                        INSERT INTO users (username, password, first_name, last_name)
                        VALUES (%s, %s, %s, %s)
                        ''', (username, password, firstname, lastname, ))
            cur.execute('''
                        SELECT * FROM users
                        ''')
            rows = cur.fetchall()
            return rows
