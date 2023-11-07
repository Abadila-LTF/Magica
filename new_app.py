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
vertical_jump= 18
max_images = 13
ENTER_P =[50, 243]
SEARCH_P= [308, 136]
SELECT_PATIENT_P= [518, 248]
DOSSIER_P= [1293, 300]
DOWNLOAD_PDF_P= [1300, 410]
AUTRE_DOCUMENTS_P= [270, 422]
VIEW_ALL_P= [348, 693]
TO_SELECT_ALL_P= [1030, 566]
FINAL_P= [1067, 96]
EXIT1_P= [1059, 26]
EXIT2_P= [1335, 8]
CHECK_1_POINT= [1180, 240]
CHECK_1_POINT_COLOR= [255, 156, 28]
CHECK_2_POINT= [15, 476]
CHECK_2_POINT_COLOR= [242, 242, 242]
CHECK_2_POINT_MAX= 100
REDIS_HOST= '35.195.67.154'
REDIS_PORT= 6379
REDIS_PASS= 'UmVkaVNwQFNz'
CHANNEL_NAME= 'ish-MAGIKA-SCRAPING-BOT2'
SEARCH_DIR= r"C:\GestiCab\Export"
IMG_CHEK = 'doc.png'
IMG_CHEK2 = 'doc2.png'
PDF_CHEK  = [704,410]
logging.basicConfig(filename='script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
log_redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, decode_responses=True)
SEARCH_IMAGE = '2.png'
DOWNLOAD_PDF_P_IMAGE = '5.png'
TO_SELECT_ALL_P_IMAGE = '6.png'
HEADER_IMAGE_PATH = 'out6.png'
FINAL_P_IMAGE = '7.png'
EXIT1_P_IMAGE= '8.png'
LOADING_IMAGE= '9.png'
DOSSIER_P_IMAGE = '3.png'
AUTRE_DOCUMENTS_P2 = [52,426]
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
def send_log_to_redis(LOGGING_CHANNEL_NAME  , log_record):
    log_redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, decode_responses=True)
    log_redis_client.publish(LOGGING_CHANNEL_NAME, log_record)


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
    ll = []
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
    l = [i for i in pyautogui.locateAllOnScreen(image,confidence=0.9)]
    return True if len(l) != 0 else False

def image_exist2(image):
    l = [i for i in pyautogui.locateAllOnScreen(image,confidence=0.9)]
    return False if len(l) != 0 else True
    
def check_how_many_elements_are_checked(image):
    l = [i for i in pyautogui.locateAllOnScreen(image,confidence=0.9)]
    return len(l)

def check_how_many_elements_are_checked2(image):
    l = [i for i in pyautogui.locateAllOnScreen(image)]
    return len(l)

def cheky_dossier():
    if not image_exist(DOSSIER_P_IMAGE):
        if not image_exist(EXIT1_P_IMAGE):
            return False
        im = pyautogui.locateOnScreen(EXIT1_P_IMAGE)
        pyautogui.click(im)
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
        logging.info(f"Processing dossier: {ipp}")
        CHECK_1 = False
        CHECK_2 = False
        CHECK_3 = False
        INSCREEN = False
        """ CHECK """
        """
        if not image_exist(SEARCH_IMAGE):
            return False
        """
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
        if chek == False :
            return False
        move_to_point_cor(DOSSIER_P)
        while True :
            if line_is_blank([822,40], 90 , 10) :
                break


        while image_exist2(IMG_CHEK) and image_exist2(IMG_CHEK2) :
            print(image_exist2(IMG_CHEK) , image_exist2(IMG_CHEK2))
        time.sleep(1)
        INSCREEN = True
        if check_point(CHECK_1_POINT,CHECK_1_POINT_COLOR) :
            """ CHECK """
            if not image_exist(DOWNLOAD_PDF_P_IMAGE):
                cheky_pdf()
            move_to_point_cor(DOWNLOAD_PDF_P)
            pyautogui.doubleClick()
            poit_is_changed(PDF_CHEK)
            time.sleep(1)
            CHECK_1 = True
        move_to_point_cor(AUTRE_DOCUMENTS_P)
        time.sleep(0.5)
        num_documents = documents_count(CHECK_2_POINT,10 ,CHECK_2_POINT_MAX)
        print(num_documents)
        if num_documents >= 1:
                move_to_point_cor(VIEW_ALL_P)
                time.sleep(0.5)
                move_to_point_cor(TO_SELECT_ALL_P)
                time.sleep(0.5)
                
                while check_how_many_elements_are_checked2(HEADER_IMAGE_PATH) < num_documents:
                    with pyautogui.hold('ctrl'):
                        pyautogui.press( 'a')
                    time.sleep(0.5)
                print(check_how_many_elements_are_checked2(HEADER_IMAGE_PATH))
                print(2222)
                time.sleep(1)
                move_to_point_cor(FINAL_P)
                poit_is_changed([963,394])

                time.sleep(1.5)
                move_to_point_cor(EXIT1_P)
                CHECK_2 = True






        move_to_point_cor(AUTRE_DOCUMENTS_P2)
        time.sleep(0.5)
        num_documents = documents_count(CHECK_2_POINT,10 ,CHECK_2_POINT_MAX)
        print(num_documents)
        if num_documents >= 1:
                move_to_point_cor(VIEW_ALL_P)
                time.sleep(0.5)
                move_to_point_cor(TO_SELECT_ALL_P)
                time.sleep(0.5)
                
                while check_how_many_elements_are_checked2(HEADER_IMAGE_PATH) < num_documents:
                    with pyautogui.hold('ctrl'):
                        pyautogui.press( 'a')
                    time.sleep(0.5)
                print(check_how_many_elements_are_checked2(HEADER_IMAGE_PATH))
                print(2222)
                time.sleep(1)
                move_to_point_cor(FINAL_P)
                poit_is_changed([963,394])

                time.sleep(1.5)
                move_to_point_cor(EXIT1_P)
                CHECK_3 = True


                

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
        else :
            print("not OKEY patirent without documents")
            logging.info(f"Processing of dossier {ipp} is complete - Ptient Without Documents")
            send_log_to_redis("LOGGING_CHANNEL" ,f"INFO : Processing of dossier {ipp} is complete - Ptient Without Documents")


def main():
        parser = argparse.ArgumentParser(description="Process dossiers")
        parser.add_argument("--input-file", required=True, help="Path to the input file")
        args = parser.parse_args()

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
    
if __name__ == "__main__":
    main()
