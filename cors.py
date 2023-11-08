from pynput.mouse import Listener
import json

# Define the button names and their corresponding coordinates
button_order = [
    "ENTER_P",
    "SEARCH_P",
    "SELECT_PATIENT_P",
    "DOSSIER_P",
    "CHECK_1_POINT",
    "DOWNLOAD_PDF_P",
    "PDF_CHEK",
    "AUTRE_DOCUMENTS_P",
    "CHECK_2_POINT",
    "CHECK_2_POINT_MARGE",
    "VIEW_ALL_P",
    "TO_SELECT_ALL_P",
    "FINAL_P",
    "EXIT1_P",
    "AUTRE_DOCUMENTS_P2",
    "VIEW_ALL_P",
    "TO_SELECT_ALL_P",
    "FINAL_P",
    "EXIT1_P",
    "EXIT2_P"
]


click_coordinates = {}


def on_click(x, y, button, pressed):
    if pressed:
        if button_order:
            button_name = button_order.pop(0)
            if button_name not in click_coordinates:
                click_coordinates[button_name] = []
            click_coordinates[button_name].append(x)
            click_coordinates[button_name].append(y)
            print(f"Clicked {button_name}.")
        else:
            print("All buttons clicked. Press Ctrl+C to stop.")


with Listener(on_click=on_click) as listener:
    print("Click on the buttons in the specified order.")
    print("Press Ctrl+C to stop.")
    try:
        listener.join()
    except KeyboardInterrupt:
        pass



click_coordinates['REDIS_HOST']= '35.195.67.154'
click_coordinates['REDIS_PORT']= 6379
click_coordinates['REDIS_PASS']= 'UmVkaVNwQFNz'
click_coordinates['CHANNEL_NAME']= 'ish-MAGIKA-SCRAPING-BOT2'
click_coordinates['SEARCH_DIR']= r"C:\GestiCab\Export"
click_coordinates['SEARCH_IMAGE'] = '2.png'
click_coordinates['DOWNLOAD_PDF_P_IMAGE'] = '5.png'
click_coordinates['TO_SELECT_ALL_P_IMAGE'] = '6.png'
click_coordinates['HEADER_IMAGE_PATH'] = 'out6.png'
click_coordinates['FINAL_P_IMAGE']= '7.png'
click_coordinates['EXIT1_P_IMAGE']= '8.png'
click_coordinates['LOADING_IMAGE']= '9.png'
click_coordinates['DOSSIER_P_IMAGE'] = '3.png'
click_coordinates['IMG_CHEK'] = 'doc.png'
click_coordinates['IMG_CHEK2'] = 'doc2.png'
click_coordinates['vertical_jump']= click_coordinates['CHECK_2_POINT_MARGE'][1] - click_coordinates['CHECK_2_POINT'][1]
click_coordinates['max_images'] = 13

with open('button_coordinates2.json', 'w') as json_file:
    json.dump(click_coordinates, json_file)

print("Button coordinates saved to button_coordinates.json")
