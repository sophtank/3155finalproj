from repositories.db import get_pool


#deletes a drive from the database
def deleteDrive(drive_id):
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            # Delete associated comments first
            cur.execute('''
                        DELETE FROM comments
                        WHERE drive_id = %s
                        ''', [drive_id])

            # Then delete associated likes
            cur.execute('''
                        DELETE FROM likes
                        WHERE drive_id = %s
                        ''', [drive_id])

            # Then delete the drive
            cur.execute('''
                        DELETE FROM drive
                        WHERE drive_id = %s
                        ''', [drive_id])

            if cur.rowcount == 0: 
                raise Exception(f"Drive with id {drive_id} not found")
            
            return True