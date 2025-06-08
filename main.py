from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
import os
import psycopg2
from db import get_connection
from etl import run_etl  # Make sure this is your ETL logic file
from send_email import send_failure_email  # the helper abov
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Email config (use environment variables in production!)
SENDER_EMAIL = os.getenv('SENDER_EMAIL'),
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD'),
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL'),

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files allowed.")
    
    os.makedirs('data', exist_ok=True)
    file_location = os.path.join('data', file.filename)

    try:
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)

        # Call the ETL function
        run_etl(file_location)

        return {"info": f"File '{file.filename}' uploaded and processed successfully."}
    except Exception as e:
        # Send failure email
        subject = "ETL Process Failure Notification"
        body = f"ETL failed for file {file.filename}.\nError: {str(e)}"
        send_failure_email(subject, body, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL)

        raise HTTPException(status_code=500, detail=f"Error during upload or processing: {e}")


@app.get("/status")
def status():
    return {"status": "API is running!"}

@app.get("/total_minutes")
def total_minutes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SUM(minutes_watched) FROM engagement")
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    return {"total_minutes_watched": result or 0}

@app.get("/top_courses")
def top_courses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT course_name, SUM(minutes_watched) AS total
        FROM engagement
        GROUP BY course_name
        ORDER BY total DESC
        LIMIT 3
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"course": r[0], "total_minutes": r[1]} for r in rows]

@app.get("/daily_engagement")
def daily_engagement():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT date, SUM(minutes_watched)
        FROM engagement
        GROUP BY date
        ORDER BY date
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"date": str(r[0]), "total_minutes": r[1]} for r in rows]

@app.get("/average_scores")
def average_scores():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT course_name, AVG(quiz_score)
        FROM engagement
        GROUP BY course_name
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"course": r[0], "avg_score": round(r[1], 2)} for r in rows]
