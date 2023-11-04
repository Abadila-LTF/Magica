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
import re


ENTER_P =[50, 243]
SEARCH_P= [308, 136]
SELECT_PATIENT_P= [518, 248]
DOSSIER_P= [1293, 300]
DOWNLOAD_PDF_P= [1300, 410]
AUTRE_DOCUMENTS_P= [270, 422]
VIEW_ALL_P= [348, 693]
TO_SELECT_ALL_P= [1030, 600]
FINAL_P= [1089, 121]
EXIT1_P= [1077, 55]
EXIT2_P= [1335, 8]
CHECK_1_POINT= [1180, 240]
CHECK_1_POINT_COLOR= [255, 156, 28]
CHECK_2_POINT= [20, 477]
CHECK_2_POINT_COLOR= [242, 242, 242]
CHECK_2_POINT_MAX= 100
REDIS_HOST= '35.195.67.154'
REDIS_PORT= 6379
REDIS_PASS= 'UmVkaVNwQFNz'
CHANNEL_NAME= 'ish-MAGIKA-SCRAPING-BOT2'
SEARCH_DIR= r"C:\GestiCab\Export"


logging.basicConfig(filename='script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
log_redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, decode_responses=True)


def send_log_to_redis(LOGGING_CHANNEL_NAME  , log_record):
    log_redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, decode_responses=True)
    log_redis_client.publish(LOGGING_CHANNEL_NAME, log_record)
def move_to_point(l):
    pyautogui.moveTo(x=l[0], y=l[1])
    pyautogui.click()
    time.sleep(1)
def move_to_point2(l):
    pyautogui.moveTo(x=l[0], y=l[1])
    pyautogui.click()
    time.sleep(2)
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
def check_point(point, color, check_type, chunk_size, max_val):
    ll=[]
    if check_type == True:
        ww = pyautogui.pixelMatchesColor(point[0], point[1], color)
        return pyautogui.pixelMatchesColor(point[0], point[1], color)
    if check_type == False:
        max_val = max_val or pyautogui.size()
        jump = (max_val - point[0]) / chunk_size
        for i in range(chunk_size):
            x = point[0] + i * jump
            y = point[1]
            ll.append(pyautogui.pixel(int(x), y))
        if len(list(set(ll))) != 1 :
                return False
        return True



NOT_FOUND=[]
def do_work(ipp):
    try:
        logging.info(f"Processing dossier: {ipp}")
        CHECK_1 = False
        CHECK_2 = False
        INSCREEN = False
        move_to_point(SEARCH_P)
        pyautogui.doubleClick()
        pyautogui.hotkey('delete')
        _workaround_write(ipp)
        pyautogui.hotkey('enter')
        time.sleep(1)
        move_to_point(SELECT_PATIENT_P)
        move_to_point(DOSSIER_P)
        while True :
            if not check_point([822,40],CHECK_2_POINT_COLOR ,False , 10 , 90) :
                break
        
        INSCREEN = True
        """ Chek 1 """
        time.sleep(2)
        if check_point(CHECK_1_POINT,CHECK_1_POINT_COLOR ,True,10,111) :
            move_to_point2(DOWNLOAD_PDF_P)
            time.sleep(2)
            CHECK_1 = True
        move_to_point(AUTRE_DOCUMENTS_P)
        """ Chek 2 """
        test = check_point(CHECK_2_POINT,CHECK_2_POINT_COLOR ,False , 10 , CHECK_2_POINT_MAX)
        print(test)
        if test == False :
            pyautogui.moveTo(x=VIEW_ALL_P[0], y=VIEW_ALL_P[1])
            pyautogui.click()
            curent = pyautogui.pixel(350,140)
            while True :
                if pyautogui.pixel(350,140) != curent and pyautogui.pixel(350,140) != (244,244,244) :
                    break

            move_to_point(TO_SELECT_ALL_P)
            with pyautogui.hold('ctrl'):
                pyautogui.press( 'a')
            pyautogui.moveTo(x=FINAL_P[0], y=FINAL_P[1])
            pyautogui.click()
            curent = pyautogui.pixel(927,396)
            while True :
                if pyautogui.pixel(927,396) != curent :
                    break
            time.sleep(1)
            move_to_point(EXIT1_P)
            CHECK_2 = True
        move_to_point(EXIT2_P)
        if CHECK_1 or CHECK_2 :
            result = check_folders_with_prefix(SEARCH_DIR, ipp)
            if result  :
                print("OKEY")
                logging.info(f"Processing of dossier {ipp} is complete")
                send_log_to_redis("LOGGING_CHANNEL" ,f"INFO : Processing of dossier {ipp} is complete")
            else :
                print("OKEY but not okey")
                logging.warning(f"Processing of dossier {ipp} is complete But Folder Not Found")
                send_log_to_redis("LOGGING_CHANNEL" ,f"WARNING : Processing of dossier {ipp} is complete But Folder Not Found")
                NOT_FOUND.append(ipp)
        else :
            print("not OKEY patirent without documents")
            logging.info(f"Processing of dossier {ipp} is complete - Ptient Without Documents")
            send_log_to_redis("LOGGING_CHANNEL" ,f"INFO : Processing of dossier {ipp} is complete - Ptient Without Documents")

    except Exception as e:
        if INSCREEN :
            move_to_point(EXIT2_P)
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
