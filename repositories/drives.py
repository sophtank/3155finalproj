from repositories.db import get_pool
from psycopg.rows import dict_row

def create_drive(user,vehicle_id, mileage, duration, title, caption, photo,date):
    with get_pool().connection() as cur:
        cur.execute('''
                    INSERT INTO drives(user, vehicle_id, mileage, duration, title, caption, photo, date)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING *
                    ''', (user, vehicle_id, mileage, duration, title, caption, photo, date))
        return cur.fetchall()
        
