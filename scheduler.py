import os
from apscheduler.schedulers.blocking import BlockingScheduler

current_path = os.getcwd()
target_file = os.path.join(current_path, "posting_macro_v2_0.py")
python_path = "/usr/bin/python3" 

# os.system(f"{python_path} {target_file}")

def run_target_file():
    os.system(f"{python_path} {target_file}")

print("Scheduler is running...")
sched = BlockingScheduler()
#sched.add_job(run_target_file, 'cron', day_of_week='sat,sun,mon,tue', hour=3, minute=00)
sched.add_job(run_target_file, 'cron', day_of_week='sat,sun,mon,tue', hour=3, minute=00)
sched.start()
