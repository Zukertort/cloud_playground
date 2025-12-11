import subprocess
import logging
import sys
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

def trigger_pipeline():
    """
    Triggers the external run_pipeline.py script.
    """
    logger.info("SCHEDULER: Triggering ML Pipeline...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, "../../../"))
    pipeline_dir = os.path.join(root_dir, "pipeline")
    script_path = os.path.join(pipeline_dir, "run_pipeline.py")

    if not os.path.exists(script_path):
        logger.error(f" Pipeline script not found at: {script_path}")
        return

    try:
        subprocess.run(
            [sys.executable, "run_pipeline.py"], 
            cwd=pipeline_dir, 
            check=True
        )
        logger.info("SCHEDULER: Pipeline execution successful.")
    except subprocess.CalledProcessError as e:
        logger.error(f"SCHEDULER: Pipeline failed with exit code {e.returncode}")
    except Exception as e:
        logger.error(f"SCHEDULER: System error: {e}")

def start_scheduler():
    if not scheduler.get_job("ml_pipeline"):
        scheduler.add_job(
            trigger_pipeline, 
            'interval',
            #seconds=30, # Comment when not debugging
            hours=1,   # Uncomment when not debugging
            id="ml_pipeline",
            replace_existing=True
        )
    
    scheduler.start()
    logger.info("Scheduler started. Job 'ml_pipeline' registered (1h interval).")

def stop_scheduler():
    scheduler.shutdown()
    logger.info("Scheduler shut down.")