#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# create_org_fits_files_none.py
# Created on Tue Jun 18, 2024
# Last updated on Tue Jun 18, 2024
#                                   by
#                               Ed Tedesco
#                      Planetary Science Institute
#                     1700 E. Fort Lowell, Suite 106
#                            Tucson, AZ 85719
# 
# See https://www.w3schools.com/python/python_ref_string.asp and
# https://note.nkmk.me/en/python-str-extract/ for string methods
# 
# Use ONLY for images with no LOISVER.
# 
# This code creates *.hdr files in the /hdr directory, for use by add_wcs_none.py.
# Before running check for, and delete, corrupt or calibration images.
# This code is hardwired to execute from D:\LONEOS\wd | /mnt/d/LONEOS/wd
# 
# Code was revised on 2023-03-03 to check for and correct differences between
# the date portion of keywords FILENAME and DATE-OBS in favor of the 
# DATE-OBS value.
# 
# Input:  Original YYMMDD_nnn.fits files
# Output: org_fits_files.txt, in D:\LONEOS\wd, containing the filenames of the
#         input files plus, in D:\LONEOS\wd\hdr, YYMMDD_nnn.hdr header files
#
import os
import time
from MontagePy.main import mGetHdr
from os import system, name
# 
# define clear screen function
def clear():
    #Clear the screen before starting.

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
# End of def clear()

# Main Program

# Clear the screen
clear()

# Start execution time counter
start_time = time.process_time()

# Write all the original YYMMDD_nnn.fits file names into the executing 
# directory's text file org_fits_files.txt
with open('org_fits_files.txt', 'w') as f:
    from pathlib import Path
    dir_org = Path(".")
    pathlist = Path(dir_org).glob('**/*.fits')
    for path in pathlist:
        # because path is object convert it to string
        in_fits = str(path)
        print(in_fits, file=f)
f.close()
# pause = input('Exit create_org_fits_files_none.py, at line 67. Press any key to continue.')
#
'''
# Create and fill FITS filename array with dummy values
fits_files_array = []
for x in range(999):
    fits_files_array.append('abc')
#
# Load filenames from file org_fits_files.txt into the Python list "Lines" 
f = open('org_fits_files.txt', 'r')
Lines = f.readlines()
count = 0
f.close()
#
# Get the total number of relevant filenames (count), strip off the /n at
# their ends, and load them into the List Array org_fits_files[]. The file-
# names for each of the "count" files to be processed, i.e, have their header
# files created, can then be referenced by org_fits_files[1] through [count].
for x in range(999):
    fits_files_array.append('abc')
#print(fits_files[0:18])
for line in Lines:
    count += 1
# removing the new line characters
    fits_files = line.rstrip()
    fits_files_array[count] = fits_files
#    print(fits_files)
#    print(fits_files_array[count])
#print("Number of files to process:", count)
# print(org_fits_files[12])
#
# Run the following on each of the non-bias file names in fits_files_array[],
# i.e., on fits_files_array[11] through fits_files_array[count+1]
# THERE MUST BE NO BIAS OR OTHER CALIBRATION FILES PRESENT!
last = count + 1
for i in range(1,last):
#    print('fits_files_array[',i,'] =',fits_files_array[i])
    in_fits = fits_files_array[i]
    fits_file_date = in_fits[0:8].strip() # Example 051113_1
    exp_num = in_fits[8:12]               # Example _011
    hdr_name = fits_file_date+"a"+exp_num+".hdr"
    dir_path_hdr_name = "/mnt/d/LONEOS/wd/hdr/"+hdr_name
#    print(fits_file_date,exp_num,hdr_name,dir_path_hdr_name)
    rtn1 = mGetHdr(in_fits, dir_path_hdr_name)
#    print(in_fits,rtn1)
    print(fits_file_date,exp_num,hdr_name,dir_path_hdr_name)
#clear()
print(' ')
execution_time = time.process_time() - start_time
rate = (count)/execution_time
execution_time = f'{float(execution_time):.3f}'
rate = f'{float(rate):.3f}'
print ('Time to process',count,'images was', execution_time, "seconds"\
, rate, '(images/sec)', )
'''