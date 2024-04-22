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
        
def edit_tag_values(drive_id, commute, near_death_experience, carpool, mostly_highway, mostly_backroads):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            UPDATE
                                tags
                            SET
                                commute = %(commute)s,
                                near_death_experience = %(near_death_experience)s,
                                carpool = %(carpool)s,
                                mostly_highway = %(mostly_highway)s, 
                                mostly_backroads = %(mostly_backroads)s
                            WHERE
                                drive_id = %(drive)s
                            ''', {'commute': commute, 'near_death_experience': near_death_experience, 'carpool': carpool, 'mostly_highway': mostly_highway, 'mostly_backroads': mostly_backroads, 'drive': drive_id})
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