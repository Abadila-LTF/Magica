import shutil
import os
def check_folders_with_prefix2(parent_directory, prefix):
    with os.scandir(parent_directory) as entries:
        for entry in entries:
            if entry.is_dir() and entry.name.startswith(prefix):
                return entry.path
    return None
def copy_folder_with_prefix(parent_directory, prefix, destination_path):

    source_path = check_folders_with_prefix2(parent_directory, prefix)
    print(source_path)


    if not source_path:
        raise ValueError(f"No folder found with prefix '{prefix}' in directory '{parent_directory}'.")

    folder_name = source_path.split('/')[-1]
    dist = destination_path+'/'+folder_name
    os.mkdir(dist)
    shutil.copytree(source_path, dist, dirs_exist_ok=True)

source_directory = "/Users/abadila/Desktop/MAGIKA_SCRAPER/yoo"
prefix = "test"
destination_path = "/Users/abadila/Desktop/MAGIKA_SCRAPER/yoo2"

copy_folder_with_prefix(source_directory, prefix, destination_path)
