import subprocess
import time
import sys
import os

# Define the sequence of scripts to run
PIPELINE_STEPS = [
    #("Ingestion", "ingest.py"),
    #("Transformation (Dollar Bars)", "transform_dollar_bars.py"),
    #("Labeling (Triple Barrier)", "labeling.py"),
    ("Feature Engineering", "feature_engineering.py"),
    ("Training (XGBoost)", "train.py")
]

def run_step(step_name, script_name):
    print(f"\n========================================")
    print(f"STARTING: {step_name}")
    print(f"========================================")
    start_time = time.time()
    
    # We run the script as a separate process
    # sys.executable ensures we use the same python interpreter
    try:
        result = subprocess.run(
            [sys.executable, script_name], 
            check=True, # Raises error if script fails
            capture_output=False # Let the script print to console
        )
        duration = time.time() - start_time
        print(f"FINISHED: {step_name} in {duration:.2f} seconds.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FAILED: {step_name} failed with exit code {e.returncode}.")
        return False
    except Exception as e:
        print(f"ERROR: Could not run {step_name}: {e}")
        return False

def main():
    
    total_start = time.time()
    
    for name, script in PIPELINE_STEPS:
        if not os.path.exists(script):
            print(f"ERROR: Script {script} not found!")
            sys.exit(1)
            
        success = run_step(name, script)
        if not success:
            print("\n PIPELINE ABORTED DUE TO ERROR.")
            sys.exit(1)
            
    total_time = time.time() - total_start
    print(f"\n PIPELINE COMPLETED SUCCESSFULLY in {total_time:.2f} seconds. ")

if __name__ == "__main__":
    main()