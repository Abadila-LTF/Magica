import pyautogui
import time
import redis
import pandas as pd
import pickle
import pyperclip
import argparse
import logging
import os
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)

ENTER_P = config["ENTER_P"]
SEARCH_P = config["SEARCH_P"]
SELECT_PATIENT_P = config["SELECT_PATIENT_P"]
DOSSIER_P = config["DOSSIER_P"]
DOWNLOAD_PDF_P = config["DOWNLOAD_PDF_P"]
AUTRE_DOCUMENTS_P = config["AUTRE_DOCUMENTS_P"]
VIEW_ALL_P = config["VIEW_ALL_P"]
TO_SELECT_ALL_P = config["TO_SELECT_ALL_P"]
FINAL_P = config["FINAL_P"]
EXIT1_P = config["EXIT1_P"]
EXIT2_P = config["EXIT2_P"]
CHECK_1_POINT = config["CHECK_1_POINT"]
CHECK_1_POINT_COLOR = config["CHECK_1_POINT_COLOR"]
CHECK_2_POINT = config["CHECK_2_POINT"]
CHECK_2_POINT_COLOR = config["CHECK_2_POINT_COLOR"]
CHECK_2_POINT_MAX = config["CHECK_2_POINT_MAX"]
REDIS_HOST = config["REDIS_HOST"]
REDIS_PORT = config["REDIS_PORT"]
REDIS_PASS = config["REDIS_PASS"]
CHANNEL_NAME = config["CHANNEL_NAME"]
SEARCH_DIR = config["SEARCH_DIR"]

"""
ENTER_P = [50, 250]
SEARCH_P = [290, 135]
SELECT_PATIENT_P = [300, 260]
DOSSIER_P = [1860, 310]
DOWNLOAD_PDF_P = [1860, 415]
AUTRE_DOCUMENTS_P = [200, 470]
VIEW_ALL_P = [350, 1010]
TO_SELECT_ALL_P = [1310, 785]
FINAL_P = [1340, 300]
EXIT1_P = [1335, 230]
EXIT2_P = [1890, 10]

CHECK_1_POINT =  [1340, 300]
CHECK_1_POINT_COLOR = (130, 135, 144)
CHECK_2_POINT  =  [1340, 300]
CHECK_2_POINT_COLOR = (130, 135, 144)
CHECK_2_POINT_MAX= 50
REDIS_HOST = '35.195.67.154'
REDIS_PORT = 6379
REDIS_PASS = 'UmVkaVNwQFNz'
CHANNEL_NAME = 'ish-MAGIKA-SCRAPING' 
SEARCH_DIR =  "/Users/abadila/Desktop" 
"""
logging.basicConfig(filename='script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
log_redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, decode_responses=True)


def send_log_to_redis(LOGGING_CHANNEL_NAME  , log_record):
    log_redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, decode_responses=True)
    log_redis_client.publish(LOGGING_CHANNEL_NAME, log_record)
def move_to_point(l):
    pyautogui.moveTo(x=l[0], y=l[1])
    pyautogui.click()
    time.sleep(1)
def _workaround_write(text):
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    pyperclip.copy('')
def check_folders_with_prefix(parent_directory, prefix):
    with os.scandir(parent_directory) as entries:
        for entry in entries:
            if entry.is_dir() and entry.name.startswith(prefix):
                return True  
    return False 
def check_point(point, color, check_type, chunk_size=10, max_val=None):
    if check_type == 0:
        return pyautogui.pixelMatchesColor(point[0], point[1], color)
    else:
        max_val = max_val or pyautogui.size()
        jump = (max_val - point[0]) / chunk_size
        for i in range(chunk_size):
            x = point[0] + i * jump
            y = point[1]
            if not pyautogui.pixelMatchesColor(x, y, color):
                return False
        return True



NOT_FOUND=[]
def do_work(ipp):
    try:
        logging.info(f"Processing dossier: {ipp}")
        CHECK_1 = False
        CHECK_2 = False
        move_to_point(SEARCH_P)
        pyautogui.doubleClick()
        pyautogui.hotkey('delete')
        _workaround_write(ipp)
        pyautogui.hotkey('enter')
        time.sleep(1)
        move_to_point(SELECT_PATIENT_P)
        move_to_point(DOSSIER_P)
        """ Chek 1 """
        if check_point(CHECK_1_POINT,CHECK_1_POINT_COLOR ,0) :
            move_to_point(DOWNLOAD_PDF_P)
            pyautogui.click()
            time.sleep(2)
            CHECK_1 = True
        move_to_point(AUTRE_DOCUMENTS_P)
        """ Chek 2 """
        if check_point(CHECK_2_POINT,CHECK_2_POINT_COLOR ,1 , 10 , CHECK_2_POINT_MAX) :
            move_to_point(VIEW_ALL_P)
            move_to_point(TO_SELECT_ALL_P)
            with pyautogui.hold('ctrl'):
                pyautogui.press( 'a')
            move_to_point(FINAL_P)
            pyautogui.click()
            time.sleep(2)
            move_to_point(EXIT1_P)
            CHECK_2 = True
        move_to_point(EXIT2_P)
        if CHECK_1 or CHECK_2 :
            result = check_folders_with_prefix(SEARCH_DIR, ipp)
            if result  :
                logging.info(f"Processing of dossier {ipp} is complete")
                send_log_to_redis("LOGGING_CHANNEL" ,f"INFO : Processing of dossier {ipp} is complete")
            else :
                logging.warning(f"Processing of dossier {ipp} is complete But Folder Not Found")
                send_log_to_redis("LOGGING_CHANNEL" ,f"WARNING : Processing of dossier {ipp} is complete But Folder Not Found")
                NOT_FOUND.append(ipp)
        else :
            logging.info(f"Processing of dossier {ipp} is complete - Ptient Without Documents")
            send_log_to_redis("LOGGING_CHANNEL" ,f"INFO : Processing of dossier {ipp} is complete - Ptient Without Documents")
    except Exception as e:
        logging.error(f"Error processing dossier {ipp}: {str(e)}")
        send_log_to_redis("LOGGING_CHANNEL" , f"ERROR : Error processing dossier {ipp}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Process dossiers")
    parser.add_argument("--input-file", required=True, help="Path to the input file")
    args = parser.parse_args()
    try:
        r = pd.read_excel(args.input_file)
        r = r["Dossier"]
        r = r.tolist()
        r = list(set(r))
        counter = 1
        max_count = len(r)
        with open('WorkingOn.pkl', 'wb') as fp:
            pickle.dump(r, fp)
            logging.info('Pickle saved successfully to file')
            send_log_to_redis("LOGGING_CHANNEL" , f"INFO : Pickle saved successfully to file")
        move_to_point(ENTER_P)
        for ipp in r:
            do_work(ipp)
            logging.info(f"Progress: {counter}/{max_count}")
            send_log_to_redis(CHANNEL_NAME , f"Progress: {counter}/{max_count}")
            counter += 1
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        send_log_to_redis("LOGGING_CHANNEL" , f"ERROR : An error occurred: {str(e)}")
    with open('NOT_FOUND.pkl', 'wb') as fp:
        pickle.dump(NOT_FOUND, fp)
        logging.info('NOT FOUND Pickle saved successfully to file')

if __name__ == '__main__':
    main()
