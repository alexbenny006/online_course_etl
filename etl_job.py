# etl_job.py

import time
from etl import run_etl

if __name__ == '__main__':
    print("🚀 Starting daily ETL job...")
    while True:
        run_etl()
        print("✅ ETL job completed. Sleeping for 24 hours.")
        time.sleep(86400)  # 24 hours in seconds
