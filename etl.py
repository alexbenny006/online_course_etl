# etl.py

import csv
from db import get_connection, create_tables

def run_etl(file_path: str):
    conn = get_connection()
    cur = conn.cursor()

    create_tables()

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cur.execute("""
                INSERT INTO engagement (id, user_id, course_name, minutes_watched, quiz_score, date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                row['id'],
                row['user_id'],
                row['course_name'],
                int(row['minutes_watched']),
                float(row['quiz_score']),
                row['date']
            ))

    conn.commit()
    cur.close()
    conn.close()
