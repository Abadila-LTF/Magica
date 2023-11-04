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
import yaml


with open('env.yml', 'r') as config_file:
    config_data = yaml.safe_load(config_file)
    

ENTER_P = config_data['ENTER_P']
SEARCH_P = config_data['SEARCH_P']
SELECT_PATIENT_P = config_data['SELECT_PATIENT_P']
DOSSIER_P = config_data['DOSSIER_P']
DOWNLOAD_PDF_P = config_data['DOWNLOAD_PDF_P']
AUTRE_DOCUMENTS_P = config_data['AUTRE_DOCUMENTS_P']
VIEW_ALL_P = config_data['VIEW_ALL_P']
TO_SELECT_ALL_P = config_data['TO_SELECT_ALL_P']
FINAL_P = config_data['FINAL_P']
EXIT1_P = config_data['EXIT1_P']
EXIT2_P = config_data['EXIT2_P']
CHECK_1_POINT = config_data['CHECK_1_POINT']
CHECK_1_POINT_COLOR = config_data['CHECK_1_POINT_COLOR']
CHECK_2_POINT = config_data['CHECK_2_POINT']
CHECK_2_POINT_COLOR = config_data['CHECK_2_POINT_COLOR']
CHECK_2_POINT_MAX = config_data['CHECK_2_POINT_MAX']
REDIS_HOST = config_data['REDIS_HOST']
REDIS_PORT = config_data['REDIS_PORT']
REDIS_PASS = config_data['REDIS_PASS']
CHANNEL_NAME = config_data['CHANNEL_NAME']
SEARCH_DIR = config_data['SEARCH_DIR']
max_images = config_data['max_images']
vertical_jump = config_data['vertical_jump']
COMPILED_CHEK_POINT = config_data['COMPILED_CHEK_POINT']
DUMMY_IMAGE = config_data['DUMMY_IMAGE']
BACK_COLOR = config_data['BACK_COLOR']
IMAGES_UPLOADED_POINT = config_data['IMAGES_UPLOADED_POINT']
PDF_CHECK_POINT = config_data['PDF_CHECK_POINT']

"""
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
max_images = 
vertical_jump=
COMPILED_CHEK_POINT = [822,40]
DUMMY_IMAGE = [350,140]
BACK_COLOR = (244,244,244)
IMAGES_UPLOADED_PIONT = [927,396]
PDF_CHEK_POINT=[]
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
        jump = (max_val - point[0]) / chunk_size
        for i in range(chunk_size):
            x = point[0] + i * jump
            y = point[1]
            ll.append(pyautogui.pixel(int(x), y))
        if len(list(set(ll))) != 1 :
                return False
        return True


def images_check(point,chunk_size, max_val):
    number_of_images = 0
    for j range(max_images):    
        ll=[]
        jump = (max_val - point[0]) / chunk_size
        for i in range(chunk_size):
            x = point[0] + i * jump
            y = point[1] + j * vertical_jump
            ll.append(pyautogui.pixel(int(x), int(y)))
        if len(list(set(ll))) == 1 :
                number_of_images+=1
    return number_of_images


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
            if not check_point(COMPILED_CHEK_POINT,CHECK_2_POINT_COLOR ,False , 10 , 90) :
                break
        INSCREEN = True
        """ Chek 1 """
        time.sleep(2)
        if check_point(CHECK_1_POINT,CHECK_1_POINT_COLOR ,True,10,111) :
            move_to_point2(DOWNLOAD_PDF_P)
            while True :
                if not check_point(PDF_CHEK_POINT,CHECK_2_POINT_COLOR ,False , 10 , 90) :
                    break
            time.sleep(1)
            CHECK_1 = True
        move_to_point(AUTRE_DOCUMENTS_P)
        """ Chek 2 """
        number_of_documents = images_check(CHECK_2_POINT, 10 , CHECK_2_POINT_MAX)
        if number_of_documents > 0:
            pyautogui.moveTo(x=VIEW_ALL_P[0], y=VIEW_ALL_P[1])
            pyautogui.click()
            curent = pyautogui.pixel(DUMMY_IMAGE[0],DUMMY_IMAGE[1])
            while True :
                if pyautogui.pixel(DUMMY_IMAGE[0],DUMMY_IMAGE[1]) != curent and pyautogui.pixel(DUMMY_IMAGE[0],DUMMY_IMAGE[1]) != BACK_COLOR :
                    if number_of_documents > 2 :
                        time.sleep(2)
                    break
            move_to_point(TO_SELECT_ALL_P)
            with pyautogui.hold('ctrl'):
                pyautogui.press( 'a')
            pyautogui.moveTo(x=FINAL_P[0], y=FINAL_P[1])
            pyautogui.click()
            curent = pyautogui.pixel(IMAGES_UPLOADED_PIONT[0],IMAGES_UPLOADED_PIONT[1])
            while True :
                if pyautogui.pixel(IMAGES_UPLOADED_PIONT[0],IMAGES_UPLOADED_PIONT[1]) != curent :
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
