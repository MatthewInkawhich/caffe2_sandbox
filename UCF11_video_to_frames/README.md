The scripts in this directory process the UCF11 dataset.

They should be run in this order:

1. mpg_to_jpgs.py
   - This script will convert each of the mpg videos in the downloaded UCF11
     dataset to a sequence of frames saved as jpg images. None of the other 
     scripts will work if this has not been run.
     ** ONLY DONE ONCE PER SAMPLING RATE **

2. create_key_file.py
   - This script creates the key file for the UCF11 dataset. 

3. create_jpg_dictionary_file.py
   - This script will iterate through the UCF11 jpg dataset created in step 1
     and create a full dictionary, noting the full path to the jpg and the 
     label according to the key file from 2.

4. split_full_dictionary.py
   - This script will input the full dictionary from step 3, shuffle it, then
     save a percentage of the entries to a train dictionary file and the rest
     to a test dictionary

5. Optional: jpgs_to_opticalflow.py
   - This script walks through the UCF11 jpg dataset created in step 1 and 
     computes the dense optical flow between each adjacent frame. The optical
     flow images are saved in the UCF11 jpg directory and each optical flow
     is saved as a horizontal output jpg and a vertical output jpg
