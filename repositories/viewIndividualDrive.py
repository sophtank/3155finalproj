from repositories.db import get_pool
from psycopg.rows import dict_row

def get_individual_drive_by_id(drive_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''
                           SELECT
                                u.first_name,
                                v.make,
                                v.model,
                                v.year,
                                d.milage,
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