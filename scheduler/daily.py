import time
import datetime
import subprocess
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("daily_scheduler.log", encoding="utf-8")
    ]
)

def run_ingestion_pipeline():
    logging.info("Starting scheduled daily ingestion pipeline...")
    # Get absolute path to the workspace root
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    run_script = os.path.join(workspace_root, "ingestion", "run.py")
    
    if not os.path.exists(run_script):
        logging.error(f"Ingestion runner script not found at: {run_script}")
        return

    try:
        # Run ingestion/run.py inside the workspace directory
        result = subprocess.run(
            [sys.executable, run_script],
            cwd=workspace_root,
            capture_output=True,
            text=True,
            check=True
        )
        logging.info("Daily ingestion pipeline finished successfully.")
        logging.info(f"Runner Output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing daily ingestion pipeline (exit code {e.returncode}):")
        logging.error(e.stderr)
    except Exception as ex:
        logging.error(f"Unexpected error running ingestion: {ex}")

def start_scheduler():
    target_hour = 10
    target_minute = 0
    logging.info(f"Daily scheduler initialized. Target execution time: {target_hour:02d}:{target_minute:02d} AM daily.")

    while True:
        now = datetime.datetime.now()
        # Calculate time until next 10:00 AM execution
        target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
        
        if now >= target_time:
            # If 10:00 AM has passed today, schedule for tomorrow
            target_time += datetime.timedelta(days=1)
            
        wait_seconds = (target_time - now).total_seconds()
        logging.info(f"Next ingestion scheduled at: {target_time.strftime('%Y-%m-%d %H:%M:%S')}. Sleeping for {wait_seconds:.1f} seconds...")
        
        # Sleep until scheduled time
        time.sleep(wait_seconds)
        
        # Execute ingestion pipeline
        run_ingestion_pipeline()
        
        # Sleep for a minute to ensure we don't double trigger
        time.sleep(60)

if __name__ == "__main__":
    try:
        start_scheduler()
    except KeyboardInterrupt:
        logging.info("Daily scheduler stopped by user.")
    except Exception as e:
        logging.error(f"Scheduler crashed: {e}")
