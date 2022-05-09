import os
import shutil

current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'images')
if os.path.exists(final_directory):
    shutil.rmtree(final_directory)	