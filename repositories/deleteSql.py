from repositories.db import get_pool


#deletes a drive from the database
def delete_drive(username, drive_id):
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        DELETE FROM drive
                        WHERE username = %s AND drive_id = %s
                        ''', (username, drive_id)
                        )
            conn.commit()