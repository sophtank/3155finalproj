from repositories.db import get_pool
from psycopg.rows import dict_row
        

#checks if the username and password match with the database
def login(username, password) -> list[dict[str, any]]:
    with get_pool().connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT username FROM users
                        WHERE username = %s AND password = %s
                        ''', (username, password))
            rows = cur.fetchall()
            return rows

#checks if a username is taken
def checkIFUserExists(username) -> list[dict[str, any]]:
    with get_pool().connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT username FROM users
                        WHERE username = %s
                        ''', (username,))
            rows = cur.fetchall()
            return rows

#if the username is not taken then the user is signed up
def SignUp(username, password, firstname, lastname) -> list[dict[str, any]]:
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        
                        INSERT INTO users (username, password, first_name, last_name)
                        VALUES (%s, %s, %s, %s)
                        ''', (username, password, firstname, lastname))
 
