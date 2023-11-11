import subprocess
import time
import redis
from datetime import datetime, timedelta
import pyautogui

REDIS_HOST= '35.195.67.154'
REDIS_PORT= 6379
REDIS_PASS= 'UmVkaVNwQFNz'
CHANNEL_NAME= 'ish-MAGIKA-SCRAPING-BOT2'

def run_script(script_path):
    process = subprocess.Popen(['python', script_path])
    return process

def is_process_alive(process):
    return process.poll() is None

def kill_process(process):
    process.terminate()

def take_screenshot():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'screenshot_{timestamp}.png'
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print(f'Screenshot saved: {filename}')

if __name__ == "__main__":
    redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, decode_responses=True)
    pubsub = redis_conn.pubsub()
    pubsub.subscribe(CHANNEL_NAME)
    last_message_time = datetime.now()
    script_path = 'app2.py'
    script_process = run_script(script_path)
    while True:
        message = pubsub.get_message()
        if message and message['type'] == 'message':
            print(f"Received message: {message['data']}")
            last_message_time = datetime.now()
        
        if not is_process_alive(script_process):
            take_screenshot()
            print('Restarting ..')
            kill_process(script_process)
            script_process = run_script(script_path)
            last_message_time = datetime.now()
        elapsed_time = datetime.now() - last_message_time
        if elapsed_time > timedelta(minutes=1):
            take_screenshot()
            print('Restarting ..')
            kill_process(script_process)
            script_process = run_script(script_path)
            last_message_time = datetime.now()
        time.sleep(5)
