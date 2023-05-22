import os
import glob
import pandas as pd

def get_all_files_together(folder_path, new_folder_path, name_file):
    os.chdir(folder_path)

    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    combined_csv.to_csv(new_folder_path + "/" + name_file, index=False, encoding='utf-8', mode='w')
    
    return combined_csv