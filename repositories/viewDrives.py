from repositories.db import get_pool
from psycopg.rows import dict_row

def get_all_drives():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''
                           SELECT
                            u.first_name,
                            d.date,
                            d.mileage,
                            d.photo,
                            d.drive_id
                           FROM 
                           drive d
                           JOIN
                           users u
                           on
                           d.username = u.username
                           ''')
            return cursor.fetchall()