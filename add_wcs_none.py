#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Program add_wcs_none.py
# Purpose: Puts keywords, including those required for WCS, into the cropped
#          images' headers.
#                                   by
#                               Ed Tedesco
#                      Planetary Science Institute
#                     1700 E. Fort Lowell, Suite 106
#                            Tucson, AZ 85719
#
# Created on Thu Sep 08 2022
# Updated Tue Nov 08 2022, Tue Jan 10 2023, Thu Feb 02 2023, Wed Feb 08 2023,
# Tue Feb 21 2023, Mon Feb 27 2023, Fri Mar 03 2023, Thu Mar 16 2023,
# Thu Apr 13 2023, Fri May 31 2024 
# Modified for LOIS none images on Tue Jun 11 2024
# Last updated Mon Jul 15 2024
#
# THIS CODE MUST BE RUN FROM A miniconda3 montage30 Ubuntu TERMINAL since it
# uses routines from MontagePy that only run in this environment. It is run by
# entering ' python add_wcs_none.py ' from the /mnt/d/LONEOS/wd/none directory
# 
# Input:  Files like YYMMDD_nnn.hdr and cropped versions YYMMDDa_nnn.fits
#         with the former in /mnt/d/LONEOS/wd/none/hdr and the latter in 
#         /mnt/d/LONEOS/wd/none
# Output: WCS embedded images (YYMMDDa_nnn.fits), header files in the format
#         YYMMDDa_nnn_wcs.hdr, and the Image Data Table YYMMDD_all.tbl all in
#         the executable directory where the WCS embedded images
#         (YYMMDDa_nnn.fits) overwrite the input cropped images with the same
#         filenames.
#
#  NOTES: 1) This code ONLY WORKS for images from LOIS none because
#            the Dec image center in the _1 and _2 headers refers to the 
#            southern edge of the _1 image but the northern edge of the _2 image. 
#            Hence, the corrections to the actual center Dec of the cropped
#            images are the same absolute value but differ in its sign.
#         2) The YYMMDDa_nnn.hdr files were created from the ORIGINAL images
#            and therefore have incorrect keyword values for some of those in
#            the CROPPED images. For example, the NAXIS1 value for the original
#            images is 2098 while the correct value for the cropped images is
#            2046. And the CRPIX2 value for the original images is 2140.5 but
#            the correct value for the cropped images is 2048.5.
#            The (correct) NAXIS1 value for the input cropped image is not
#            changed by this code and the CRPIX2 value is changed to the
#            correct value in the code (in line 240). All other keywords 
#            obtained from the .hdr files are correct.
#
# To process images for a given night, e.g., YYMMDD, files like YYMMDDa_nnn.hdr
# and YYMMDDa_nnn.fits are required. The .hdr files are produced by
# create_hdr_none_ds.py and in D:\LONEOS\wd\none\hdr and the .fits files are the
# cropped original files to which WCS keywords need to be added and which are
# located in the executable directory which is D:\LONEOS\wd\none
# 
# The first input to this code is the number of images to be processed, i.e., the
# number of *.hdr files The next block of code puts this number in num_images and
# the directory where the *.hdr files are located in ...wd\none\hdr
#
import os
import time
from astropy.io import fits
from MontagePy.main import mGetHdr, mImgtbl
from os import system, name
#from decimal import Decimal, ROUND_UP
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

# Function to read a specific line from HDU using the readline() function
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
# 
# Main Program
# 
# Clear the screen
clear()
# Assign directory name
dirname = '/mnt/d/LONEOS/wd/none'
os.chdir(dirname) # NOTE: / instead of \
# #print("add_wcs_none.py line 106: The current working directory is", os.getcwd())
# pause = input('Press ENTER to continue..')
# exit()
#
#   Enter CRVAL1 offset (in degrees)
#
# offset = input('Enter CRVAL1 offset (in degrees): ')
# 
# Start execution time counter
start_time = time.process_time()
# The first input to this code is the number of images to be processed, i.e.,
# the number of *.hdr files, and the directory where they are located put into
# hdr_dir The following for block then puts this number in num_images
hdr_dir = os.getcwd()+'/hdr/'
fits_dir = os.getcwd()
fits_wcs_hdr_dir = os.getcwd()+'/wcs_hdr/'
# print('\nadd_wcs_none.py Line 122: hdr directory =',hdr_dir)
# print('fits directory =',fits_dir,'and fits_wcs_hdr_dir =',fits_wcs_hdr_dir)
# #pause = input('Line 124 Press ENTER to continue..')
num_images = 0

for path in os.listdir(hdr_dir):
# check if current path is a file
    if os.path.isfile(os.path.join(hdr_dir, path)):
        num_images += 1
#print('The number of images in', hdr_dir, '(num_images) =', num_images)
num_images = num_images + 1
# #print(' ')
# #print('Line 134 num_images + 1 =',num_images)
# pause = input('Press ENTER to continue..')
# Define and initialize *.hdr array variable
fits_files_array = list(range(1,num_images+1))

fileNames = os.listdir(hdr_dir)

count = 0

for line in fileNames:
    count += 1
#   print('count =',count)
#   removing the new line characters
    fits_files = line.rstrip()
    fits_files_array[count] = fits_files
#   print(fits_files_array[count])
    
#print(fits_files_array[1],'...',fits_files_array[i])
for i in range(1,num_images):

    fits_file_i = fits_files_array[i]
    # #print(" ")
    # #print("Line 156 FITS file =",fits_file_i)
    hdr_file = fits_file_i[0:11]+'hdr'
    hdrfile = hdr_dir+hdr_file # Header file [i] path qualified name
#   fits_files_array[i] holds the names of the input image files
    fits_files_array[i] = fits_file_i[0:11]+'fits'
    # #print('Line 161',i,"Header file =",hdr_file," fits_files_array[i] =",fits_files_array[i])
    # #print('Line 162',i,"FITS file =",hdr_file) # Supposed to be YYMMDDa_nnn.fits
    # #pause = input('Press Enter to continue.')
# 
#   Get the number of lines in the header of image YYMMDD_nnn.fits
#    with open(hdrfile, 'r') as fp:
#        hdr_lines = len(fp.readlines())
#        print('Total Number of lines in file', hdrfile, '=', hdr_lines)
#    fp.close()
#    pause = input('Press Enter to continue.')
    LOISVERS = 'none' 
    # #print('Line 172', fits_files_array[i], 'LOISVERS= ', LOISVERS)
# 
    OBSERVER = 'Unspecified'
    # #print('Line 175 OBSERVER=', OBSERVER)
    # #pause = input('Press ENTER to continue..')
# 
    card62= read_line(hdrfile, 62)
    COMMENTLINE = card62[0:7]
    # #print('Line 180: COMMENTLINE =',COMMENTLINE)
    # #pause = input('Press ENTER to continue..')
    if COMMENTLINE == 'COMMENT':
        SKIP = 'NO'
        # #print('Line 184: COMMENTLINE =',COMMENTLINE,'SKIP =',SKIP)
        # #pause = input('Press ENTER to continue..')
    else:
        SKIP = 'YES'
        # #print('Line 188: COMMENTLINE =',COMMENTLINE,'SKIP =',SKIP)
        # #pause = input('Press ENTER to continue..')
 
    card23= read_line(hdrfile, 23) # DATE_UT is on the same line in both cases
    DATE_UT = card23[10:19]
    YY = card23[11:13]
    MM = card23[14:16]
    DD = card23[17:19]
    DATE_UT = YY+MM+DD
    card20= read_line(hdrfile, 20) # CCDPICNO is on the same line in both cases
    CCDPICNO= card20[27:30].strip()
    if len(CCDPICNO) == 1: CCDPICNO = '00'+CCDPICNO
    if len(CCDPICNO) == 2: CCDPICNO = '0'+CCDPICNO
    FILENAME = DATE_UT+'_'+CCDPICNO+'.fits'
    WCSFILENAME = DATE_UT+'a_'+CCDPICNO+'.fits'
    # #print('Line 203 DATE_UT =', DATE_UT, 'CCDPICNO =', CCDPICNO)
    # #print('FILENAME =', FILENAME, 'WCSFILENAME =', WCSFILENAME)        
    # #pause = input('Press ENTER to continue.')
    if SKIP == 'NO':
        card51 = read_line(hdrfile, 51)
        CRVAL1 = float(card51[20:31].strip()) # + float(offset)
        card52 = read_line(hdrfile, 52)
        CRVAL2 = float(card52[20:31].strip())
    else:
        card52 = read_line(hdrfile, 52)
        CRVAL1 = float(card52[20:31].strip()) # + float(offset)
        card53 = read_line(hdrfile, 53)
        CRVAL2 = float(card53[20:31].strip())
    
    # #print('Line 217: SKIP = ', SKIP, 'CRVAL1 = ', CRVAL1, 'CRVAL2 = ', CRVAL2)
    # #pause = input('Press ENTER to continue.')
    if SKIP == 'NO':
        AIRMASS = read_line(hdrfile, 46)
    else:
        AIRMASS = read_line(hdrfile, 47)
# Below IF statement checks whether the AIRMASS value is a string, '1.35', or a
# (right justified) float, 1.280000E+00 and if a float it rounds it to two decimals
    AIRMASS_type = AIRMASS[10]
    if AIRMASS_type == "'":
        AIRMASS = AIRMASS[11:16]
    else:
        AIRMASS = AIRMASS[18:31]
        AIRMASS = f'{float(AIRMASS):.2f}'
#    Above formatting needed for airmass to always have two decimals
# 
#    print('AIRMASS_type =', AIRMASS_type, 'AIRMASS =', AIRMASS)
#    print('Line 234 AIRMASS =', AIRMASS)
#    pause = input('Above AIRMASS values read from header. Press ENTER to continue..')
#
    OBJECT = read_line(hdrfile, 21) # OBJECT is on the same line in both cases
    OBJECT = OBJECT[11:23]
#    print(card36)
    # #print('Line 241 OBJECT =', OBJECT)
    # #pause = input('Press ENTER to continue..')
# 
    EXPTIME = read_line(hdrfile, 25) # EXPTIME is on the same line in both cases
    # EXPTIME = EXPTIME[18:30] 
    EXPTIME = f'{float(EXPTIME[18:30]):.1f}'
#    Above formatting needed for EXPTIME to always have one decimal
#    print(card40)
    # #print('Line 249 EXPTIME =', EXPTIME)
    # #pause = input('Press ENTER to continue..')
#     
    UTCSTART = read_line(hdrfile, 33) # UTCSTART is on the same line in both cases
    UTCSTART = UTCSTART[11:21].strip("'")
#    print(card39)
    # #print('Line 255 UTCSTART =', UTCSTART)
    # #pause = input('Press ENTER to continue..')
#   Code below writes the indicated keywords into the header
    fits_file = fits_files_array[i]
    # #print('Line 259 fits_file =', fits_file)
    # #pause = input('Press ENTER to continue..')    
#    
    with fits.open(WCSFILENAME, mode='update') as f:
        for hdu in f:
            hdu.header['BSCALE'] = 1
            hdu.header['BZERO'] = 32768
            hdu.header['DATAMAX'] = 65535
            hdu.header['DATAMIN'] = 0
            hdu.header['LOISVERS'] = LOISVERS
            hdu.header['OBSERVER'] = OBSERVER
            hdu.header['DATE'] = DATE_UT
            hdu.header['CTYPE1'] = 'RA---TAN'
            hdu.header['CTYPE2'] = 'DEC--TAN'
            hdu.header['CRPIX1'] = 1023.5
            hdu.header['CRPIX2'] = 2048.5
            hdu.header['AIRMASS'] = round(float(AIRMASS),3)
            hdu.header['FILENAME'] = WCSFILENAME
            hdu.header['OBJECT'] = OBJECT
            hdu.header['EXPTIME'] = round(float(EXPTIME),3) 
            hdu.header['UTCSTART'] = UTCSTART
            hdu.header['LONPOLE'] = 180.0
            hdu.header['LATPOLE'] = 0.0
            hdu.header['CRVAL1'] = CRVAL1 
            hdu.header['CRVAL2'] = CRVAL2
            hdu.header['CD1_1'] = +0.000703 # from original image header
            hdu.header['CD1_2'] =-1.814E-06 # from original image header
            hdu.header['CD2_1'] =-1.952E-06 # from original image header
            hdu.header['CD2_2'] =-0.000703  # from original image header
#            FILENAME = fits_files_array[i]
        f.flush()
#print('num_images =',num_images)
# #print('Line 290: Finished writing the indicated keywords into the header')
# #pause = input('Press ENTER to continue..')
for i in range(1,num_images):
    FILENAME = fits_files_array[i]
#    FNMAIN = FILENAME[0:10]+'a_wcs.hdr'
    FNMAIN = FILENAME[0:6]+'a'+FILENAME[6:10]+'_wcs.hdr'
#    print('Line 296: fits_files_array[i] = ',i,fits_files_array[i])
#    print('FILENAME = ', FILENAME) 
#    print('Header File (FNMAIN) = ', FNMAIN)
#    with open(FNMAIN, mode='write') as f:
#        f.write()
#    print(hdr)
#        f.close() 
    mGetHdr(FILENAME,FNMAIN)
#    pause = input('Line 304: Press ENTER to continue..')
"""
mImgtbl scans a specified dir for FITS images with WCS information and writes
information, including all four “corner” coordinate pairs, to a file. The
data for each image appears on its own line and the output is in a special
format. 

The contents, and order, of the items written to the Imgtbl contain many, but 
not all, of the header keywords and add numerous additional items, e.g., the 
four “corner” coordinate pairs.
"""    
img_tbl_name = FILENAME[0:6]+'_all.tbl'
FILENAME = fits_files_array[1]
first_wcs = FILENAME[0:10]+'a_wcs.hdr'

print('\nadd_wcs_none.py Line 320: Images with embedded WCS are in:',fits_dir)
print('and header files and the image Table, in the same directory,','are in',
      '\nfiles:',first_wcs,'through', FNMAIN, 'and', img_tbl_name)

mImgtbl(fits_dir, img_tbl_name)

#clear()
print(' ')
execution_time = time.process_time() - start_time
rate = (num_images-1)/execution_time
execution_time = f'{float(execution_time):.3f}'
rate = f'{float(rate):.3f}'
print ('Time to process',num_images-1,'images was', execution_time, "seconds"\
, rate, '(images/sec)', )
print(' ')
print('Last line of add_wcs_none.py') 
#pause = input('Press any key to return to line 267 in \
#create_pds_files_none_ds.sh')