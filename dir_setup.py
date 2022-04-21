import os
import shutil

# intakes directory as a string, deletes if present, replaces
def dir_setup(directory):
    # delete all contents of output folder if present
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)