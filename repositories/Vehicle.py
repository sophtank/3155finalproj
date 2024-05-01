from repositories.db import get_pool
from psycopg.rows import dict_row
        

#gets the details of the vehicle of the user
def get_vehicles(username) -> list[dict[str, any]]:
    with get_pool().connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT 
                            make, model, year, vehicle_id, color
                        FROM 
                            vehicle
                        WHERE username = %s
                        ''', (username,))
            rows = cur.fetchall()
            return rows

#gets the owner of the vehicle
def get_owner(id):
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        SELECT 
                            username
                        FROM 
                            vehicle
                        WHERE vehicle_id = %s
                        ''', (id,))
            rows = cur.fetchone()
            return rows

#adds a vehicle to the database
def add_vehicle(vehicle_id, username, make, model, year, color) -> list[dict[str, any]]:
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        INSERT INTO vehicle (vehicle_id, username, make, model, year, color)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ''', (vehicle_id, username, make, model, year, color))
            

#edits a vehicle in the database
def edit_vehicle(vehicle_id, username, make, model, year, color) -> bool:
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        UPDATE vehicle
                        SET make = %s, model = %s, year = %s, color = %s
                        WHERE vehicle_id = %s AND username = %s
                        ''', (make, model, year, color, vehicle_id, username))
            if cur.rowcount == 0: 
                raise Exception(f"Vehicle with id {vehicle_id} not found")
            return True
        
#deletes a vehicle from the database
def delete_vehicle(vehicle_id, username):
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                        DELETE FROM vehicle
                        WHERE vehicle_id = %s AND username = %s
                        ''', (vehicle_id, username))
            if cur.rowcount == 0: 
                raise Exception(f"Vehicle with id {vehicle_id} not found")
            return True

#gets the details of the vehicle by id
def get_vehicle_by_id(vehicle_id):
    with get_pool().connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT 
                            make, model, year, color
                        FROM 
                            vehicle
                        WHERE vehicle_id = %s
                        ''', (vehicle_id,))
            rows = cur.fetchone()
            return rows

#gets the drives of the vehicle
def get_drives(vehicle_id):
    with get_pool().connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                        SELECT 
                            drive_id
                        FROM 
                            drive
                        WHERE vehicle_id = %s
                        ''', (vehicle_id,))
            rows = cur.fetchall()
            return rows