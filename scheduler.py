import os
from apscheduler.schedulers.blocking import BlockingScheduler
import configparser
import datetime
from itertools import cycle

# Paths for the script and configuration file
current_path = os.getcwd()
target_file = os.path.join(current_path, "posting_macro_v2_0.py")
config_file = os.path.join(current_path, "config.ini")
python_path = "/usr/bin/python3"  # Path to Python interpreter

# User schedule
user_schedule = {
    "Saturday": [
        {"name": "우지형", "id": "dnwlzz", "password": "baghcai!123"},
    ],
    "Sunday": [
        {"name": "한지연", "id": "hjy9171", "password": "xpsltmwhgdk6742!"},
    ],
    "Monday": [
        {"name": "유병경", "id": "ybk707", "password": "qudrud8706!"},
    ],
    "Tuesday": [
        {"name": "김수민", "id": "sumin0928", "password": "rlatnqkr928@"},
#        {"name": "나영아", "id": "euttm", "password": "a123456789*"},
    ],
}

def update_config_file(user_id, user_password):
    """
    Update the config.ini file with the given user credentials.
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    # Update the LOGIN section
    config['LOGIN']['id'] = user_id
    config['LOGIN']['password'] = user_password

    # Write the updated configuration back to the file
    with open(config_file, 'w') as configfile:
        config.write(configfile)

def run_target_file():
    """
    Run the target Python file.
    """
    os.system(f"{python_path} {target_file}")

def get_next_scheduled_day(current_day):
    """
    Find the next scheduled day in the user schedule based on the current day.
    """
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_cycle = cycle(days_of_week)
    
    # Advance the cycle to the current day
    while next(day_cycle) != current_day:
        continue
    
    # Find the next day with a schedule
    for next_day in day_cycle:
        if next_day in user_schedule:
            return next_day

def schedule_jobs():
    """
    Schedule jobs for each user based on the current day of the week.
    """
    # Determine the current day of the week
    current_day = datetime.datetime.now().strftime('%A')  # e.g., 'Monday', 'Tuesday', etc.
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Scheduler started.")
    print(f"Today is {current_day}.")

    if current_day in user_schedule:
        users = user_schedule[current_day]
        print(f"Scheduled users for today ({current_day}):")
        for user in users:
            print(f"- {user['name']} (ID: {user['id']})")

        sched = BlockingScheduler()

        for user in users:
            user_id = user["id"]
            user_password = user["password"]

            # Schedule a job for each user
            sched.add_job(
                update_and_run,
                args=[user_id, user_password],
                trigger="cron",
                hour=3,
                minute=0,
            )

        sched.start()
    else:
        # Find the next scheduled day
        next_day = get_next_scheduled_day(current_day)
        print(f"No users scheduled for today ({current_day}). The next schedule is on {next_day}.")

        users = user_schedule[next_day]
        print(f"Scheduled users for {next_day}:")
        for user in users:
            print(f"- {user['name']} (ID: {user['id']})")

        sched = BlockingScheduler()

        for user in users:
            user_id = user["id"]
            user_password = user["password"]

            # Schedule a job for the users on the next scheduled day
            sched.add_job(
                update_and_run,
                args=[user_id, user_password],
                trigger="date",
                run_date=(datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour=3, minute=0, second=0),
            )

        sched.start()

def update_and_run(user_id, user_password):
    """
    Update the config.ini file and run the target script.
    """
    print(f"Running for user: {user_id}")
    update_config_file(user_id, user_password)
    run_target_file()

if __name__ == "__main__":
    schedule_jobs()
