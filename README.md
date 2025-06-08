# 📘 Online Course Engagement ETL & Dashboard

## 📁 Folder Structure
```
online_course_etl/
├── data/
│   └── course_engagement.csv      # Source data file
├── templates/
│   └── index.html                 # File upload form
├── db.py                          # Database models
├── etl.py                         # One-time ETL script
├── etl_job.py                     # Daily loop ETL job
├── main.py                        # FastAPI API
├── dashboard.py                   # Streamlit dashboard
├── requirements.txt               # Dependencies
└── README.md                      # Project info
```

## 🔄 ETL Flow
Extract daily course engagement → Transform → Load into SQLite → Preview stats via FastAPI → Visualize with Streamlit

## ▶️ How to Run

### 1. Setup Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run ETL Once
```bash
python etl.py
```

### 3. Start ETL as Daily Job
```bash
python etl_job.py
```

### 4. Launch FastAPI Server
```bash
uvicorn main:app --reload
```

Visit: http://127.0.0.1:8000/docs

### 5. Start Streamlit Dashboard
```bash
streamlit run dashboard.py
```

## 🧠 FastAPI Endpoints

| Method | Endpoint            | Description               |
|--------|---------------------|---------------------------|
| GET    | `/`                 | Status check              |
| GET    | `/total_minutes`    | Total minutes watched     |
| GET    | `/top_courses`      | Top 3 watched courses     |
| GET    | `/daily_engagement` | Daily video engagement    |
| GET    | `/average_scores`   | Avg quiz score per course |
