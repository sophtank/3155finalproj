from repositories.db import get_pool
from psycopg.rows import dict_row

def create_drive(drive_id, vehicle_id, mileage, duration, title, caption, photo, date, user):
    with get_pool().connection() as cur:
        cur.execute('''
                    INSERT INTO drive(drive_id, vehicle_id, mileage, duration, title, caption, photo, date, username)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (drive_id, vehicle_id, mileage, duration, title, caption, photo, date, user))
        