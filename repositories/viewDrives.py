from repositories.db import get_pool
from psycopg.rows import dict_row
import datetime
import uuid

# get all drives
def get_all_drives():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''
                           SELECT
                              u.first_name, u.last_name,
                              d.title, d.date, d.mileage, d.photo,d.drive_id
                           FROM 
                              drive d
                           JOIN
                              users u
                           on
                              d.username = u.username
                           ORDER BY
                              d.date ASC
                           ''')
            return cursor.fetchall()
        
#get comments by drive id
def get_comments(drive_id: int):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''
                        SELECT  
                            d.drive_id, 
                            c.comment_id, c.username, c.comment, c.date
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
                        ''', [drive_id])
            return cursor.fetchall()
        
#make a new comment
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
    
#delete comments by comment id
def delete_comment(comment_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''
                            DELETE FROM comments
                            WHERE comment_id = %s
                        ''', [comment_id])
            

#get comment by comment id
def get_comment_by_id(comment_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''
                            SELECT 
                                comment_id 
                            FROM 
                                comments
                            WHERE comment_id = %s
                        ''', [comment_id])
            return cursor.fetchone()
    
#gets the owner of the comment by id
def get_comment_owner(comment_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''
                            SELECT 
                                username 
                            FROM 
                                comments
                            WHERE comment_id = %s
                        ''', [comment_id])
            return cursor.fetchone()

#gets the owner of the drive by id/username
def sql_is_owner(drive_id, username):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''
                            SELECT 
                                * 
                            FROM 
                                drive
                            WHERE drive_id=%s AND username=%s
                        ''', [drive_id,username])
            return cursor.fetchone()

#gets drive id by comment id 
def get_drive_id_comment(comment_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory= dict_row) as cursor:
            cursor.execute('''
                            SELECT 
                                drive_id 
                            FROM 
                                comments
                            WHERE comment_id = %s
                        ''', [comment_id])
            return cursor.fetchone()