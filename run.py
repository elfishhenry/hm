import multiprocessing
import multiprocessing.process
import subprocess
import os
from keep_alive import keep_alive

# Define the directory containing the scripts
script_dir = r"C:\Users\User\Documents\lets try making a bot again\hm"
log_file = os.path.join(script_dir, 'bot.log')

keep_alive() #this keeps the bot alive


def run_bot_commands():
    script_path = os.path.join(script_dir, 'bot_commands.py')
    subprocess.run(["python", script_path])

def run_economy():
    script_path = os.path.join(script_dir, 'economy.py')
    subprocess.run(["python", script_path])

    



if __name__ == "__main__":
    try:
        # Start the processes
        p1 = multiprocessing.Process(target=run_bot_commands)
        p2 = multiprocessing.Process(target=run_economy)
        


        p1.start()
        p2.start()
   
        
        p1.join()
        p2.join()
   
    finally:
        # Delete the log file after the processes are done
        if os.path.exists(log_file):
            os.remove(log_file)
        print("Log file deleted.")


