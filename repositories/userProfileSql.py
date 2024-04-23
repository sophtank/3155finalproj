from repositories.db import get_pool
from psycopg.rows import dict_row
        

# gets the details of the drive of the user 
def getAllDrives(username) -> list[dict[str, any]]:
    with get_pool().connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT vehicle.make, vehicle.model, drive.duration, drive.mileage, drive.drive_id
                        FROM drive
                        JOIN Vehicle ON drive.vehicle_id = Vehicle.vehicle_id
                        WHERE drive.username = %s
                        ''', (username,))
            rows = cur.fetchall()
            return rows