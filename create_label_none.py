#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Program: create_label_none.py
# Purpose: Create PDS4 Labels for LONEOS LOIS none original AND augmented images
#                                   by
#                               Ed Tedesco
#                      Planetary Science Institute
#                     1700 E. Fort Lowell, Suite 106
#                            Tucson, AZ 85719
#
# Created on   Thu 27 Jun 2024
# Last updated Fri 13 Dec 2024
# 
# Uses the keyword FILENAME, instead of DATE, to assign the DATE
# because the DATE keyword's value is often incorrect.
#
# Input:  A YYMMDD.tbl and YYMMDD_all.tbl plus template csv files with
#         file name formats YYMMDD.csv AND YYMMDDa.csv in directory
#         D:\LONEOS\wd\none together with the YYMMDD_nnn_wcs.hdr files 
#         (e.g., YYMMDDa_nnn_wcs.hdr) in directory D:\LONEOS\wd\none\wcs_hdr
#         The template csv files are created by create_pds_files_none_ds.sh
# Output: 980826.csv and 980826a.csv where 980826.csv contains label values
#         for the original image and 980826a.csv contains the 25 Label values
#         for each augmented image.
# NOTE: (The following paragraph is obsolete.)
# Run from a TCMD terminal using the alias step04. This will run
# create_labels.BTM which changes to directory D:\LONEOS\wd\none and runs:
# create_modified_tbl_file.py followed by
# C:\Users\ed_te\AppData\Local\Programs\Spyder\Python\python.exe create_label_none.py
# 
# This code must run from the directory that contains the code and the input
# files, viz., YYMMDD.tbl and template csv files with file names YYMMDD.csv and 
# YYMMDDa.csv in directory D:\LONEOS\wd\none plus the wcs.hdr files
# (e.g., 980826a_011_wcs.hdr through 980826a_458_wcs.hdr) in directory
# D:\LONEOS\wd\none\wcs_hdr
# 
# The following paragraph is obsolete.
# The modified YYMMDD.tbl is the entire .tbl file WITHOUT the three
# column header lines created in the BTM file (create_labels.BTM) that runs
# this code and the template YYMMDD.csv and YYMMDDa.csv files are .csv files
# with ONLY their header lines that are ALWAYS present in the executing
# directories because they are ALWAYS THE SAME, even for different LOIS vesions.

# The wcs.hdr files, & ONLY those files, with names like 980826a_013_wcs.hdr
# must be in a child directory named wcs_hdr of the execution directory
# D:\LONEOS\wd\none

# xml_25 "samples" are the number of Columns in the image (same as NAXIS1) and
# xml_24 "lines" are the number of Rows in the image (same as NAXIS2)
# That is, "samples" = number columns = NAXIS1 = image width and
#          "lines"   = number rows = NAXIS2 = image hight
# Definitions above are from Bea's Wed 2022-11-09 16:22 email.

#  No explicit error check is made on the input date but if the date entered
#  is not that of the required input files a Python error ends the run with
#  a "FileNotFoundError: [Errno 2] No such file or directory:" message.

# The "corner", CRVAL1 and CRVAL2 coordinates are obtained from the appropriate
# .tbl file and all other keywords are from the *wcs.hdr files whose source, 
# except for the FILENAME keyword, is the original image's header.
#
import os
import time
from os import system, name

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

# Function to read a specific line from a file using the readline() function
def read_line(fname, lnum):
    card = ''
    try:
        file = open(fname, 'r')
        lines = file.readlines()
        file.close()
    except:
        print('Error reading file:', fname)
        return
    
    total_cards = len(lines)
    if lnum > total_cards:
        print(str(total_cards) + " header cards.")
        print("Cannot read card " + str(lnum) + "!")
    else:
        card = lines[lnum - 1].rstrip("\n")
#        print("Card ", lnum, " is: ", card)
        return card
# End of def read_line()

# Main Program
# Clear the screen
clear()
#pause = input('At create_label_none.py Line 104 - Press ENTER to continue.')                                         

# Start the script execution time counter
start_time = time.process_time()

# Put the directory where the *.hdr files are located into wcs_hdr_dir
dir_format = os.getcwd()
wcs_hdr_dir = os.getcwd()+'/wcs_hdr/'
fits_dir = os.getcwd()+'/'
# print('wcs_hdr_dir =',wcs_hdr_dir)
# print('fits_dir =',fits_dir)
# pause = input('create_label_none.py Line 115 - Press ENTER to continue.')

# Get the number of images to be processed
num_images = 0
for path in os.listdir(wcs_hdr_dir):
# check if current path is a file
    if os.path.isfile(os.path.join(wcs_hdr_dir, path)):
        num_images += 1
# print('The nummber of images in', wcs_hdr_dir, '(num_images) =', num_images)
# pause = input('create_label_none.py Line 124 - Press ENTER to continue.')
# 
# The next step is to define and initialize the *.hdr array variable which
# allows the lines, aka "cards", in each *.hdr file to be extracted and
# reformatted for writing to the output *.csv files (e.g., 980826.csv and 
# 980826a.csv) from which the PDS4 Label is created. 

# Define and initialize *.hdr array variable
fits_files_array = list(range(1,num_images+2))
# print("fits_files_array[1] =",fits_files_array[1],"wcs_hdr_dir =",wcs_hdr_dir)
# pause = input('create_label_none.py Line 134 - Press ENTER to continue.')
fileNames = os.listdir(wcs_hdr_dir)
# print(fileNames)
# pause = input('create_label_none.py Line 137 - Press ENTER to continue.')
count = 0

for line in fileNames:
    count += 1
# removing the new line characters
    fits_files = line.rstrip()
    fits_files_array[count] = fits_files
#    print(count,fits_files_array[count])
#print(fits_files_array[1],'...',fits_files_array[i])
#num_lines = num_images # For use in creating corners_file.txt
# print("count = ",count)
# Open files
#
# Get the date of the images in the executable directory.
# This assumes a file of the form YYMMDDa_nnn.fits exists
# but it should since the required input includes files YYMMDD.csv,
# YYMMDDa.csv, and YYMMDD.tbl plus numerous FITS files beginning
# with YYMMDDa_nnn.fits
#
pwd=os.getcwd()
obs_date = os.listdir(pwd)[0]
# N_S = obs_date[6:8]
obs_date = obs_date[0:6]
print('pwd =', pwd)
print('obs_date =',obs_date[0:6])
# print('N_S =',obs_date[6:8])
# pause = input('create_label_none.py Line 164 - Press ENTER to continue.')
table_file = obs_date+".tbl"
print("Table filename =",table_file)
# pause = input('create_label_none.py Line 167 - Press ENTER to continue.')
tbl = open(table_file,'r')   # Table file must have ZERO column header lines!
#                              and a name of YYMMDD.tbl
# Define and initialize *.tbl array variable
tbl_line_array = list(range(1,num_images+2))   # +2 needed to avoid overfill
# print('tbl_line_array =', tbl_line_array)
# pause = input('create_label_none.py Line 173: Press ENTER to continue.')
csva_filename = obs_date+"a.csv"         # The AUGMENTED images' .csv filename
csva_file = open(csva_filename,'a')      # This file, containing ONLY its header
                                         # line, must be present before running
csv_filename = obs_date+".csv"           # The ORIGINAL images' .csv filename
csv_file = open(csv_filename,'a')        # This file containing ONLY its header
                                         # line must be present before running this script.
# pause = input('create_label_none.py Line 180: check csv files - Press ENTER to continue.')                                         
# The ORIGINAL images' YYMMDD.csv file has 9 fields (columns) while
# the AUGMENTED images' YYMMDD_none.csv file has 25 fields (columns).
# print("Table filename =",table_file,"and csv filename =",csv_filename)
# pause = input('create_label_none.py Line 184 - Press ENTER to continue.')

# An issue arose because *.tbl is 3 lines longer than num_images due to the org
# *.tbl's three header lines. Hence, because I was unable to deal with this in
# this code, those 3 lines must be deleted from the *.tbl file before running.

# print('num_images =',num_images) # The actual number of *_wcs.hdr files which
                                   # equals the number of non-header column lines
                                   # in the *.tbl file.
# pause = input('create_label_none.py Line 189 - Press ENTER to continue.')
                                 
# To get a square going clockwise starting from the "top-left" (assuming that 
# means NE) corner using the PDS4 system you have to draw a box from the top_left
# to top_right to bottom_right to bottom_left, i.e. for YYMMDD_1_011.fits,

# ra4,dec4 xml_05,xml_06 322.5880356, 10.0059880  NE
# ra1,dec1 xml_07,xml_08 319.6641607, 10.0139949  NW with ra1 = ra1 - 0.0333333 (xml_07)
# ra2,dec2 xml_09,xml_10 319.6663990,  8.5726702  SW with ra2 = ra2 - 0.0333333 (xml_09)
# ra3,dec3 xml_11,xml_12 322.5782654,  8.5646935  SE
clear()
# print ('obs_date =',obs_date) # This is the DATE of the night processed
# night_processed=input('Enter date of night processed in YYYY-MM-DD format: ')
obs_date_str=str(obs_date)
obs_date_YYYY='19'+str(obs_date_str[0:2]) # = 19 plus the first two digits of obs_date
obs_date_MM=str(obs_date_str[2:4]) # This is digits 3 and 4 of obs_date
obs_date_DD=str(obs_date_str[4:6]) # This is digits 5 and 6 of obs_date
night_processed=obs_date_YYYY+'-'+obs_date_MM+'-'+obs_date_DD
print('night_processed =',night_processed)
#pause = input('create_label_none.py line 212. Press ENTER to continue.')
for i in range(1,num_images+1):  # +1 needed to avoid not reading the last line
    tbl_line_array[i] = tbl.readline()
    tbl_line = tbl_line_array[i]
    tbl_num = tbl_line[0:8]
#    print('Line 211: Entering for i loop at i =',i,'tbl_num =',tbl_num) 
#    print('tbl_line =',tbl_line)
#    pause = input('Press ENTER to continue.')
#   The following two lines correct the coordinates of the west edge of the 
#   image to the actual RA. This accounts for the incorrect RAs in the western
#   half of each image.
#   ra1_corner = float(tbl_line[382:393]) - 0.0333333
#   ra2_corner = float(tbl_line[410:421]) - 0.0333333
    ra1_corner = float(tbl_line[382:393]) # - 0.0333333
    ra2_corner = float(tbl_line[410:421]) # - 0.0333333
# Next two lines add 360 if the expanded RA corner's RA < 0
    ra1_corner = ra1_corner if ra1_corner >= 0 else ra1_corner + 360.
    ra2_corner = ra2_corner if ra2_corner >= 0 else ra2_corner + 360.
    xml_05 = f'{(float(tbl_line[466:477])):10.6f}' # Right justified to 6 decimals
    xml_06 = f'{(float(tbl_line[480:491])):10.6f}' # Right justified to 6 decimals
    xml_07 = f'{(float(ra1_corner)):10.6f}'
    xml_08 = f'{(float(tbl_line[396:407])):10.6f}' # Right justified to 6 decimals
    xml_09 = f'{(float(ra2_corner)):10.6f}'
    xml_10 = f'{(float(tbl_line[424:435])):10.6f}' # Right justified to 6 decimals
    xml_11 = f'{(float(tbl_line[438:449])):10.6f}' # Right justified to 6 decimals
    xml_12 = f'{(float(tbl_line[452:463])):10.6f}' # Right justified to 6 decimals
    xml_19 = str(tbl_line[496:504]) # size, data_file_size
    corners_4 = xml_05+','+xml_06+','+xml_07+','+xml_08+','+xml_09+','+xml_10+','+xml_11+','+xml_12
#    print(tbl_num,corners_4)
    xml_13 = str(tbl_line[132:142]) # crval1
    xml_14 = str(tbl_line[146:156]) # crval2
#     print('crval1 =',xml_13,'crval2 =',xml_14)
#     pause = input('create_label_none.py Line 231 - Press ENTER to continue.')
# The following lines get the relevant keywords from the YYMMDDa_nnn_wcs.hdr files

    fits_file_i = fits_files_array[i]
    hdr_file = fits_file_i[0:11]+'_wcs.hdr'
    hdrfile = wcs_hdr_dir+hdr_file
    fits_files_array[i] = fits_file_i[0:6]+'a_'+fits_file_i[8:11]+'.fits'
    print(i,"Header file =",hdrfile," fits_files_array[i] =",fits_files_array[i])
    print(i,"FITS file =",fits_file_i) # fits_file_i is supposed to be YYMMDDa_nnn.fits
#    pause = input('create_label_none.py Line 253 - Press ENTER to continue.')
    card18 = read_line(hdrfile, 18) # FILENAME as '980826_001.fits'
#    card18 = fits_file_i[0:6]+'a_'+fits_file_i[7:10]+'.fits'
    print('card18 =', card18) # whose headers are in D:\LONEOS\wd\none\wcs_hdr
#    pause = input('create_label_none.py Line 251 - Press ENTER to continue.')
    xml_01 = card18[11:22].strip("'''''")+".xml" # 980826a_nnn.xml
    print('xml_01 =',xml_01)
#    pause = input('create_label_none.py Line 260 - Press ENTER to continue.')
#    xml_01 = card18[11:18]+'1a_'+card18[18:21].strip("'''''")+".xml" # 02-10
#    xml_01_No_a = card18[11:18]+'1_'+card18[18:21].strip("'''''") # 02-14
#    xml_01_No_a = card18[11:24].strip("'''''") # 02-21 [11:23] to [11,24] replaced by line below
    xml_01_No_a = card18[11:17]+ card18[18:22].strip("'''''")+'.xml' # which should be 980829_001.xml
    xml_01_aName = card18[11:22]+ '.xml' # which should be 980829a_001.xml
    print("xml_01_No_a =",xml_01_No_a," xml_01_aName =",xml_01_aName)
#    pause = input('create_label_none.py Line 267 - Press ENTER to continue.')
    xml_17_date = xml_01[0:6].strip("'''''") # 
#    xml_17 = xml_17_date+card18[18:23].strip("'''''")+".fits" # 980826_nnn.fits
#    xml_17 = card18[11:19]+card18[20:24].strip("'''''")+".fits"
#    xml_17 = card18[11:19]+'a_'+card18[20:23].strip("'''''")+".fits" # 02-10
#    xml_18 = card18[10:23].strip("'''''")+".fits" # date_nnn.fits xml_17 = card18[11:22].strip("'''''")+".fits" # source_product
    xml_17 = card18[11:17]+ card18[18:27] # source_product
#    xml_18 = card18[11:21].strip("'''''")+"a.fits" # data_file_name
#    xml_18x = card18[11:21].strip("'''''")+"a.xml" # filename for a.csv
#    xml_18 = card18[11:17].strip("'''''")+"a"+card18[17:21].strip("'''''")+".fits"
#    xml_18x = card18[11:17].strip("'''''")+"a"+card18[17:21].strip("'''''")+".xml"
    xml_18 = card18[11:17].strip("'''''")+card18[17:22].strip("'''''")+".fits"
    xml_18x = card18[11:17].strip("'''''")+card18[17:22].strip("'''''")+".xml"
#    print("xml_01 =",xml_01,", xml_17_date =",xml_17_date)
    print("xml_17 =",xml_17,", xml_18 =",xml_18,", xml_18x=",xml_18x)
    #pause = input('create_label_none.py Line 282 - Press ENTER to continue.')
#    tbl_file = card18[10:17].strip("'''''")+".tbl"
#    if i == 1: f_table = open(tbl_file, 'r')
#    print(i,xml_01,xml_17,xml_18)

#for line in f_table:
#    print(i,"Line{}: {}".format(i, line.strip()))
    
# Hardwired value title
    xml_02 = 'Augmented LONEOS Survey Image' # title
#    print(i,xml_02)

#    card12 = read_line(hdrfile, 12) # This is the DATE
#    print('card12 =',card12[11:18]) # This is the DATE
    card21 = read_line(hdrfile, 21)
#    UTCSTART42 = card21[11:19].strip("'")
    UTCSTART = card21[10:19].strip("'") # 04:53:28.0
#    print(UTCSTART42,UTCSTART)
    # print('card21 =',card21) # UTCSTART= '04:53:28.0'
    # print('UTCSTART =', UTCSTART) # 04:53:28.0
#    pause = input('Line 300: Press ENTER to continue. Last pause line.')
#   card12 = '2000-03-10' # This is a hardwired value
#   start_date_time = card12[11:30] #.strip("'''")
# The next line is needed because the time portion of DATE differs from the 
# exposure start time (UTCSTART); it is generally 1 sec later
    xml_03 = night_processed+'T'+UTCSTART # start_date_time
#    print('card12 is',card12)
    print('Line 309: start_date_time (xml_03) =', xml_03) 
    # pause = input('Press ENTER to continue.')
    card20 = read_line(hdrfile, 20)
    exposure_duration = card20[18:30] 
    exposure_duration = f'{float(card20[18:30]):.1f}'
    ssed = float(exposure_duration)/3600.
#    Above formatting needed for exposure_duration to always have one decimal
#    print('exposure_duration (sec) =', exposure_duration,'in hrs =',ssed)
#    pause = input('Line 299: Press ENTER to continue.')    
    xml_16 = exposure_duration
    stop_date = xml_03[0:11]  # Probably valid only for dates prior to 000000
    stop_time = xml_03[11:21] # Probably valid only for dates prior to 000000
#    print('Line 321: exposure_duration (xml_16) =', xml_16, 'exposure_duration =', exposure_duration)
    print('Line 322: stop_date (xml_03[0:9]) =', stop_date, 'stop_time (xml_03[11:21]) =', stop_time)
#    print('Line 323: HH, MM, SS =', stop_time[0:2], ', ', stop_time[3:5], ', ', stop_time[6:8])
    #pause = input('Press ENTER to continue.')
    HH = float(stop_time[0:2])
    MM = float(stop_time[3:5])
    SS = float(stop_time[6:8]) 
#    print('Line 326: HH, MM, SS =', HH, ', ', MM, ', ', SS)
#    pause = input('Press ENTER to continue.')    
    stop_time = round((HH + MM/60. + SS/3600.), 6) # The stop time in decimal hours
    stop_time_sec = (stop_time + ssed)*3600. # The stop time in seconds
#    print('Line 330: stop_time, stop_time_sec =', stop_time, ', ', stop_time_sec)
#    pause = input('Press ENTER to continue.')        
# The next line takes the time in seconds and outputs hour, minute, and second
# values separately, i.e., it returns a string = HH:MM:SS. For more info see
# https://www.digitalocean.com/community/tutorials/python-convert-time-hours-minutes-seconds
# Prompt user for night processed in YYYY-MM-DD format
    stop_time = time.strftime("%H:%M:%S", time.gmtime(stop_time_sec))
    # print('Line 329: night_processed =',night_processed)
    # pause = input('Press ENTER to continue.')
     
    stop_date = night_processed
#    print('Line 341: stop_date (YYYY-MM-DD) =',stop_date)
#    pause = input('Press ENTER to continue.')  
    xml_04 = stop_date+'T'+stop_time # stop_date_time
    # print(i,'stop_date =', stop_date, 'stop_time =', stop_time) 
    print(i,'stop_date_time (xml_04) =', xml_04) #, stop_time_hrs)
    #pause = input('Line 348: Press ENTER to continue.')
#    card24 = read_line(hdrfile, 24) # CRVAL1
#    xml_13 = card24[20:31]
#    print(card24)
#    print('center_ra  =', xml_13)
#    pause = input('Press ENTER to continue.') 
#    card25 = read_line(hdrfile, 25) # CRVAL2
#    xml_14 = card25[20:31]
#    print(card25)
#    print('center_dec =', xml_14)
    
    card6 = read_line(hdrfile, 6)
#    print(i,'hdrfile =', hdrfile)
    BSCALE = f'{float(card6[29:30]):.1f}'
    xml_22 = BSCALE
#    Above formatting needed for BSCALE to always have one decimal
#    print(i,fits_files_array[i], 'BSCALE= ', xml_23)

    card7 = read_line(hdrfile, 7)
#    print(i,'hdrfile =', hdrfile)
    BZERO = f'{float(card7[25:30]):.1f}'
    xml_23 = BZERO
#    Above formatting needed for BSCALE to always have one decimal
#    print(i,fits_files_array[i], 'BZERO= ', xml_24)

# Hardwired value north_clock_angle
    xml_15 = '180' # north_clock_angle Changed from 0
#    print(i,'north_clock_angle',xml_15)

# Hardwired value header_length
    xml_20 = '2880' # header_length
#    print(i,'header_length =',xml_21)

# Hardwired value image_offset
    xml_21 = '2880' # image_offset
    xml_21org = '5760' # Original image_offset Changed from 11520
#    print(i,'image_offset =',xml_22)

# Hardwired value lines
    xml_24 = '4096' # lines Changed from 2050
    xml_24org = '4146' # Original image lines Changed from 2050
#    print(i,'lines =',xml_24)
    
# Hardwired value samples
    xml_25 = '2046' # samples Changed from 4196
    xml_25org = '2098' # Original image samples Changed from 4296
#    print(i,'samples =',xml_25)  

# Write xml lines to *.csv file
    csv_01_04 = xml_18x+','+xml_02+','+xml_03+','+xml_04+',' # changed xml_01
    print(i,'xml_01 - xml_04 =',csv_01_04)                  # to xlmx_18 02/16
    csv_05_14 = corners_4+','+xml_13+','+xml_14+','
    print(i,'xml_05 - xml_14 =',csv_05_14)
    csv_15_25 = xml_15+','+xml_16+','+xml_17+','+xml_18+','+xml_19+','+xml_20\
        +','+xml_21+','+xml_22+','+xml_23+','+xml_25+','+xml_24 # switched 25 & 24
    print(i,'xml_15 - xml_25 =',csv_15_25)
    csva_line = csv_01_04 + csv_05_14 + csv_15_25
    csv_line = xml_01_No_a+','+ xml_03+','+ xml_04+','+ xml_17\
        +','+ xml_21org+','+ xml_22+','+ xml_23+','+ xml_25org+','\
        + xml_24org
    print(csv_line)
    csva_file.write(csva_line+'\n')
    csv_file.write(csv_line+'\n')
    print(i,xml_01)
#pause = input('create_label_none.py closing files. Press ENTER to continue.')
tbl.close()
csv_file.close()
csva_file.close()
#clear()
print(' ')
execution_time = time.process_time() - start_time
execution_time = f'{float(execution_time):.3f}'
print ('Time to process',num_images,'images was', execution_time, "seconds")       
#pause = input('Press ENTER to return to line 364 in create_pds_files_none_ds.sh.')