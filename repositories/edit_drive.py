from repositories.db import get_pool
from psycopg.rows import dict_row

def edit_drive_values(drive_id, mileage, duration, vehicle, title, caption):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            UPDATE
                                drive
                            SET
                                mileage = %(mileage)s,
                                duration = %(duration)s,
                                vehicle_id = %(vehicle)s,
                                title = %(title)s, 
                                caption = %(caption)s
                            WHERE
                                drive_id = %(drive)s
                            ''', {'mileage': mileage, 'duration': duration, 'vehicle': vehicle, 'title': title, 'caption': caption, 'drive': drive_id})
            return None
        
def get_drive(drive_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT
                                drive_id,
                                mileage,
                                duration,
                                vehicle_id,
                                title,
                                caption,
                                photo,
                                username
                            FROM
                                drive
                            WHERE
                                drive_id = %s
                            ''', [drive_id])
            return cursor.fetchone()
        
def get_vehicles(username):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT
                                vehicle_id,
                                make,
                                model
                            FROM
                                vehicle
                            WHERE
                                username = %s
                            ''', [username])
            return cursor.fetchall()