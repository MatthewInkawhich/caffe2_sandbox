# NAI
# This script walks throught the UCF11 jpg dataset that was created with the
#   mpg_to_jpgs script and calculates the optical flow images for each adjacent
#   frame.

import os
import glob
import cv2

# ***************************************************************
# Function to calculate dense optical flow between two adjacent frames
def calc_optical_flow(img1, img2, ofile_name_horizontal, ofile_name_vertical):

	frame1 = cv2.imread(img1)
	frame2 = cv2.imread(img2)

	f1_gray = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
	f2_gray = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

	# calculate dense optical flow
	# settings from tutorial
	# https://docs.opencv.org/3.3.1/d7/d8b/tutorial_py_lucas_kanade.html
	flow = cv2.calcOpticalFlowFarneback(f1_gray,f2_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

	h_oflow = flow[...,0]
	v_oflow = flow[...,1]

	h_oflow = cv2.normalize(h_oflow, None, 0, 255, cv2.NORM_MINMAX)
	v_oflow = cv2.normalize(v_oflow, None, 0, 255, cv2.NORM_MINMAX)

	#print h_oflow.max()
	#print h_oflow.min()
	#print h_oflow.mean()

	cv2.imwrite(ofile_name_horizontal, h_oflow)
	cv2.imwrite(ofile_name_vertical, v_oflow)



calc_optical_flow("samples/v_shooting_01_01_f0.jpg","samples/v_shooting_01_01_f6.jpg","h_out.jpg", "v_out.jpg")

exit()

# ***************************************************************
# MAIN

root_ucf_jpg_directory = os.path.join(os.path.expanduser('~'),"DukeML/datasets/UCF11/UCF11_updated_jpg_5FPS")

# for each subdirectory in root dir [ex. UCF11_updated_mpg/basketball]
for dir1 in glob.glob(root_jpg_directory + '/*'):

	# for each subdirectory in new category level directory [ex. UCF11_updated_mpg/basketball/v_shooting_01]
	for dir2 in glob.glob(dir1 + "/*"):

		# for each level 3 directory [ex. UCF11_updated_mpg/basketball/v_shooting_01/01/]
		for dir3 in glob.glob(dir2 + "/*"):

			# get an array of jpgs in the directory (these are full paths)
			jpg_arr = glob.glob(dir3 + "/jpgs/*.jpg")

			# make an array of just the file names in the jpg arr
			names = [os.path.split(img)[-1] for img in jpg_arr]

			# sort the array, this will order the jpgs by frame number
			names.sort(key = lambda x: int(os.path.splitext(x)[0].split("_")[-1][1:]))
			#print names

			# create the oflow directory for this scene if it does not exist
			#if os.path.exists(dir3 + "/oflow") == False:
			#	os.makedirs(dir3 + "/oflow")

			# select consecutive pairs of frames to calculate optical flow between
			for i in range(len(names)-1):

				frame1 = names[i]
				frame2 = names[i+1]

				# get the frame number of the second frame
				fnum2 = os.path.splitext(frame2)[0].split("_")[-1]

				# construct output file name
				ofname = os.path.splitext(frame1)[0] + "_" + fnum2 + "_" + str(i)

				print "Optical Flow( ",frame1,', ',frame2,' ) => ',ofname

				in1 = dir3 + "/jpgs/" + frame1
				in2 = dir3 + "/jpgs/" + frame2
				in3 = dir3 + "/oflow/" + ofname + "_h.jpg"
				in4 = dir3 + "/oflow/" + ofname + "_v.jpg"

				print "\tIn1: ", in1
				print "\tIn2: ", in2
				print "\tIn3: ", in3
				print "\tIn4: ", in4

			# construct the line to be written to the file
			# ex. </full/path/to/jpg> <label>
			#output = img + " " + label
			#print output
			exit()