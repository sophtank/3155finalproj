from repositories.db import get_pool
from psycopg.rows import dict_row
import datetime
import uuid

def get_all_drives():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''
                           SELECT
                            u.first_name,
                            d.date,
                            d.mileage,
                            d.photo,
                            d.drive_id
                           FROM 
                           drive d
                           JOIN
                           users u
                           on
                           d.username = u.username
                           ORDER BY
                           d.date DESC
                           ''')
            return cursor.fetchall()
        
def get_comments(drive_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''
                           SELECT 
                            d.drive_id, 
                            c.comment_id,
                            c.username, 
                            c.comment, 
                            c.date
                           FROM
                           comments c
                           JOIN
                           drive d 
                           ON 
                           d.drive_id = c.drive_id
                           WHERE
                            d.drive_id = %s
                           ORDER BY
                           c.date DESC;

                           ;
                           ''', [drive_id])
            return cursor.fetchall()
        
def make_comment(drive_id, username, comment):
    pool = get_pool()
    current_time = datetime.datetime.now()
    comment_id = uuid.uuid4()
    comment_id = str(comment_id)
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''
                INSERT INTO comments (comment_id, drive_id, username, comment, date)
                           VALUES (%s, %s, %s, %s, %s)
                           ''',[comment_id, drive_id, username, comment, current_time])
    
def delete_comment(comment_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''
                            DELETE FROM comments
                            WHERE comment_id = %s
                           ''', [comment_id])