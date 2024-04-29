from repositories.db import get_pool
from psycopg.rows import dict_row

def get_individual_drive_by_id(drive_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''
                           SELECT
                                u.first_name,
                                u.username,
                                v.make,
                                v.model,
                                v.year,
                                d.mileage,
                                d.duration,
                                d.caption,
                                d.photo,
                                d.date,
                                d.drive_id
                            FROM
                                drive d
                            INNER JOIN
                                vehicle v ON d.vehicle_id = v.vehicle_id
                            INNER JOIN
                                users u ON d.username = u.username
                            WHERE
                           drive_id = %s;
                           ''', [drive_id])
            return cursor.fetchone()
        
def get_num_likes(drive_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''              
                            SELECT COUNT(*) FROM likes 
                            WHERE
                           drive_id = %s;
                           ''', [drive_id])
            return cursor.fetchone()

def add_like(drive_id, username):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''              
                           INSERT INTO likes VALUES (%s, %s)
                           ''', [drive_id, username])

def delete_like(drive_id, username):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''              
                            DELETE FROM likes 
                           WHERE drive_id = %s AND username  = %s
                           ''', [drive_id, username])

def has_like(drive_id, username):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''              
                            SELECT * FROM likes 
                            WHERE
                           drive_id = %s AND username=%s;
                           ''', [drive_id, username])
            return cursor.fetchone()
        