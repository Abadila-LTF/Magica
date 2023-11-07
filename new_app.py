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
PDF_CHEK  = []
logging.basicConfig(filename='script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
log_redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, decode_responses=True)
SEARCH_IMAGE =
DOWNLOAD_PDF_P_IMAGE =
TO_SELECT_ALL_P_IMAGE = 
HEADER_IMAGE_PATH =
FINAL_P_IMAGE =
EXIT1_P_IMAGE=
LOADING_IMAGE=
def move_to_point_cor(l):
    pyautogui.moveTo(x=l[0], y=l[1])
    pyautogui.click()
def move_to_point_image(image_path):
    x, y = pyautogui.locateCenterOnScreen('image.png')
    pyautogui.click(x, y)
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

def documents_count(point,chunk_size, max_val):
    number_of_images = 0
    for j in range(max_images):    
        ll=[]
        jump = (max_val - point[0]) / chunk_size
        
        for i in range(chunk_size):
            x = point[0] + i * jump
            y = point[1] + j * vertical_jump
            ll.append(pyautogui.pixel(int(x), int(y)))
        if len(list(set(ll))) != 1 :
            number_of_images+=1
        else :
            break
    return number_of_images

def poit_is_changed(point,color = None):
    if color :
        curent = pyautogui.pixel(point[0],point[1])
        while True :
            if pyautogui.pixel(point[0],point[1]) != curent and pyautogui.pixel(point[0],point[1]) != color :
                return True
    else :
        curent = pyautogui.pixel(point[0],point[1])
        while True :
            if pyautogui.pixel(point[0],point[1]) != curent :
                return True
def line_is_blank(point, max_val , chunk_size):
    max_val = max_val or pyautogui.size()
    jump = (max_val - point[0]) / chunk_size
    for i in range(chunk_size):
        x = point[0] + i * jump
        y = point[1]
        ll.append(pyautogui.pixel(int(x), y))
    if len(list(set(ll))) != 1 :
            return True
    return False
    
def check_point(point, color):
    return pyautogui.pixelMatchesColor(point[0], point[1], color)

def image_exist(image):
    return True if len(pyautogui.locateAllOnScreen(image)) != 0 else False
    
def check_how_many_elements_are_checked(image):
    return len(pyautogui.locateAllOnScreen(image))

def cheky_dossier():
    if not image_exist(DOSSIER_P_IMAGE):
        if not image_exist(EXIT1_P_IMAGE):
            return False
        x,y = pyautogui.locateAllOnScreen(EXIT1_P_IMAGE)
        pyautogui.click(x,y)
        time.sleep(0.5)
        if not image_exist(DOSSIER_P_IMAGE):
            return False
        
def cheky_pdf():
    if not image_exist(VIEW_ALL_P_IMAGE):
        chek=cheky_dossier()
        if check == False :
            return False
        move_to_point_cor(DOSSIER_P)
        while True :
            if line_is_blank([822,40], 90 , 10) :
                break

def perform_ui_actions(ipp):
    try:
        logging.info(f"Processing dossier: {ipp}")
        CHECK_1 = False
        CHECK_2 = False
        INSCREEN = False
        """ CHECK """ 
        if not image_exist(SEARCH_IMAGE):
            return False
        move_to_point_cor(SEARCH_P)
        time.sleep(0.5)
        pyautogui.doubleClick()
        pyautogui.hotkey('delete')
        _workaround_write(ipp)
        pyautogui.hotkey('enter')
        time.sleep(0.5)
        move_to_point_cor(SELECT_PATIENT_P)
        """ CHECK """
        chek=cheky_dossier()
        if check == False :
            return False
        move_to_point_cor(DOSSIER_P)
        while True :
            if line_is_blank([822,40], 90 , 10) :
                break
        INSCREEN = True
        if check_point(CHECK_1_POINT,CHECK_1_POINT_COLOR) :
            """ CHECK """
            if not image_exist(DOWNLOAD_PDF_P_IMAGE):
                cheky_pdf()
            move_to_point_cor(DOWNLOAD_PDF_P)
            pyautogui.doubleClick()
            poit_is_changed(PDF_CHEK)
            CHECK_1 = True
        move_to_point_cor(AUTRE_DOCUMENTS_P)
        time.sleep(0.5)
        num_documents = documents_count(CHECK_2_POINT,10 ,CHECK_2_POINT_MAX)
        if num_documents > 1:
            move_to_point_cor(VIEW_ALL_P)
            poit_is_changed([350,140] , (244,244,244)):
            """ CHECK """
            if image_exist(TO_SELECT_ALL_P_IMAGE):
                move_to_point_cor(TO_SELECT_ALL_P)
                while check_how_many_elements_are_checked(HEADER_IMAGE_PATH) < num_documents:
                    with pyautogui.hold('ctrl'):
                        pyautogui.press( 'a')
                """ CHECK """
                if not image_exist(FINAL_P_IMAGE):
                    time.sleep(2)
                move_to_point_cor(FINAL_P)
                poit_is_changed([927,396])
                """ CHECK """
                if not image_exist(EXIT1_P_IMAGE):
                    if image_exist(LOADING_IMAGE) :
                        while image_exist(LOADING_IMAGE) :
                            time.sleep(0.5)
                move_to_point_cor(EXIT1_P)
                CHECK_2 = True
        """ CHECK """
        move_to_point_cor(EXIT2_P)
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
        move_to_point_cor(ENTER_P)
        for ipp in r:
            if perform_ui_actions(ipp)== False:
                logging.error(f"A Big error occurred, stoped!!")
                send_log_to_redis("LOGGING_CHANNEL" , f"ERROR : A Big error occurred, stoped!!")
                break
            logging.info(f"Progress: {counter}/{max_count}")
            send_log_to_redis(CHANNEL_NAME , f"Progress: {counter}/{max_count}")
            counter += 1
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        send_log_to_redis("LOGGING_CHANNEL" , f"ERROR : An error occurred: {str(e)}")
    with open('NOT_FOUND.pkl', 'wb') as fp:
        pickle.dump(NOT_FOUND, fp)
        logging.info('NOT FOUND Pickle saved successfully to file')
if __name__ == "__main__":
    main()
