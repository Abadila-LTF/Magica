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
CHECK_2_POINT= [15, 476]
CHECK_2_POINT_COLOR= [242, 242, 242]
CHECK_2_POINT_MAX= 100
REDIS_HOST= '35.195.67.154'
REDIS_PORT= 6379
REDIS_PASS= 'UmVkaVNwQFNz'
CHANNEL_NAME= 'ish-MAGIKA-SCRAPING-BOT2'
SEARCH_DIR= r"C:\GestiCab\Export"
max_images = 14
vertical_jump= 18
COMPILED_CHEK_POINT = [822,40]
DUMMY_IMAGE = [350,140]
BACK_COLOR = (244,244,244)
IMAGES_UPLOADED_PIONT = [927,396]
PDF_CHEK_POINT=[666,417]


def images_check(point,chunk_size, max_val):
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
    return number_of_images
number_of_documents = images_check(CHECK_2_POINT, 20 , CHECK_2_POINT_MAX)
print(number_of_documents)

