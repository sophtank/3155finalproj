from repositories.db import get_pool
from psycopg.rows import dict_row

def edit_drive(drive_id, milage, duration, caption):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            UPDATE
                                drive
                            SET
                                milage = {milage},
                                duration = duration {duration},
                                caption = {caption},
                            WHERE
                                drive_id = {drive_id}
                           ''')
            return None