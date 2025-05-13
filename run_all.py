import subprocess
import time

# קבצים להרצה
files_to_run = [
    "create_db.py",
    "PetFeederDataManager.py",
    "FeederRelay.py",
    "PetFeederGui.py",
    "autoFeeder.py",
    "FeedingSchedulerGui.py",
    "FeedingStatsGui.py"
]

processes = []

try:
    for i, file in enumerate(files_to_run):
        print(f"[🚀] Launching: {file}")
        if i == 0:
            subprocess.run(["python", file], check=True)  
        else:
            proc = subprocess.Popen(["python", file])
            processes.append(proc)
            time.sleep(1)  

    print("\n[✓] All components launched. Press Ctrl+C to stop.")

    # חכה שהחלונות פתוחים
    for proc in processes:
        proc.wait()

except KeyboardInterrupt:
    print("\n[!] Stopping all processes...")
    for proc in processes:
        proc.terminate()
