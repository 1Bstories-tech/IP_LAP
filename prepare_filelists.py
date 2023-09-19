# filelists
#   |-- train.txt
#   |-- test.txt

import os
import random

filelist_name = "avspeech"
path = "datasets/avspeech_landmarks"
filelists = ["train.txt", "test.txt"]

test_percent = 0.0264

# List folders in the directory
folders = os.listdir(path)
for d in folders:
    folders_in_d = os.listdir(os.path.join(path, d))

    # Set is_test to True test_percent% of the time (randomly)
    is_test = False
    if random.random() < test_percent:
        is_test = True

    for f in folders_in_d:
        # Create filelists folder if it doesn't exist
        if not os.path.exists(f"filelists/{filelist_name}"):
            os.makedirs(f"filelists/{filelist_name}")
        # If is_test is True, add to test.txt, else add to train.txt
        if is_test:
            with open(os.path.join(f"filelists/{filelist_name}", filelists[1]), "a") as test:
                test.write(os.path.join(d, f) + "\n")
        else:
            with open(os.path.join(f"filelists/{filelist_name}", filelists[0]), "a") as train:
                train.write(os.path.join(d, f) + "\n")
