from minio import Minio
import os
import psycopg2
from pathlib import Path



DB_NAME = 'preprod_db'
DB_USER = 'postgres'
DB_PASS = 'V2JyVHBOM2c3cQ=='
DB_HOST = '34.77.155.11'
DB_PORT = '32630'

conn = psycopg2.connect(
	dbname=DB_NAME,
	user=DB_USER,
	password=DB_PASS,
	host=DB_HOST,
	port=DB_PORT
)
cursor = conn.cursor()

directory_path =  "/Users/abadila/Desktop/"
MINIO_API_HOST = "minio.clinops.app"
MINIO_ACCESS_KEY = "miniouser"
MINIO_SECRET_KEY = "miniouserpass"
bucket_name = "preprod-bucket"

MINIO_CLIENT = Minio(MINIO_API_HOST, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=True)

all_items = os.listdir(directory_path)
folders = [item for item in all_items if os.path.isdir(os.path.join(directory_path, item))]


query = "SELECT id ,  ipp FROM patients"
cursor.execute(query)
p_data = cursor.fetchall()
p_data_mapper = {i[1]:i[0] for i in p_data}
folder_count = 1
prefix = "Magica_BackUp/"
file_pation_to_upload = []
for i in folders :
    if i in p_data.keys() :
        patient_id = p_data[i]
        nom = "nom"
        flag = "PRINCIPALE"
        directory = Path(i)
        files = [str(item)  for item in directory.iterdir() if item.is_file()]   
        for item in directory.iterdir() :
            if item.is_file():
                file = str(item)
                url = prefix + file
                MINIO_CLIENT.fput_object(bucket_name, url , directory_path + file )
                file_pation_to_upload.append([patient_id ,nom , flag , url])
        print(f"Moving Folder{folder_count}")
        if folder_count % 10000 == 0 :
            MINIO_CLIENT = Minio(MINIO_API_HOST, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=True)
        folder_count += 1

print("Inserting File Pation ..")
ValuresToImport = tuple([tuple(i) for i in  file_pation_to_upload])
InsertQuery = "INSERT INTO ile_patient (patient_id ,nom , flag , url) VALUES (((%s)))"
InsertQuery = cursor.mogrify(InsertQuery, (ValuresToImport,))
InsertQuery = InsertQuery.decode("utf-8")
InsertQuery = InsertQuery.replace("((((", "").replace("))))", "")
InsertQuery = InsertQuery.encode()
cursor.execute(InsertQuery)