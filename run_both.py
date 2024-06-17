import multiprocessing
import subprocess
import os

# Define the directory containing the scripts
script_dir = r"C:\Users\User\Documents\lets try making a bot again\hm\code"
log_file = os.path.join(script_dir, 'bot.log')

def run_bot_commands():
    script_path = os.path.join(script_dir, 'bot_commands.py')
    subprocess.run(["python", script_path])

def run_slash_commands():
    script_path = os.path.join(script_dir, 'slash_commands.py')
    subprocess.run(["python", script_path])

if __name__ == "__main__":
    try:
        # Start the processes
        p1 = multiprocessing.Process(target=run_bot_commands)
        p2 = multiprocessing.Process(target=run_slash_commands)

        p1.start()
        p2.start()

        p1.join()
        p2.join()
    finally:
        # Delete the log file after the processes are done
        if os.path.exists(log_file):
            os.remove(log_file)
        print("Log file deleted.")
