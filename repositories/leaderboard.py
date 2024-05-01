from repositories.db import get_pool
from psycopg.rows import dict_row

# returns the leaderboard
def get_leaders():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                        SELECT 
                            drive.username AS "Name",
                        ROUND
                            (CAST(SUM(drive.mileage) AS NUMERIC),1) 
                        AS 
                            "Miles Driven"
                        FROM 
                            drive
                        GROUP BY 
                            "Name"
                        ORDER BY 
                            "Miles Driven" DESC;''')
            return cursor.fetchall()