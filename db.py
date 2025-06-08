# db.py

import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS engagement (
            id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL,
            course_name TEXT NOT NULL,
            category TEXT NOT NULL,
            minutes_watched INTEGER NOT NULL,
            quiz_score REAL NOT NULL,
            date DATE NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    create_tables()
