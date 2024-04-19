from repositories.db import get_pool
from psycopg.rows import dict_row
        


def vehicleExists(username, make, model, year, color) -> list[dict[str, any]]:
    with get_pool().connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT make, model, year, color
                        FROM vehicle
                        WHERE username = %s AND make = %s AND model = %s AND year = %s AND color = %s
                        ''', (username, make, model, year, color))
            rows = cur.fetchall()
            return rows


#adds a vehicle to the database
def addVehicle(vehicle_id, username, make, model, year, color) -> list[dict[str, any]]:
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        INSERT INTO vehicle (vehicle_id, username, make, model, year, color)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ''', (vehicle_id, username, make, model, year, color))