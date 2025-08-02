# -*- coding: utf-8 -*-
"""
Program create_ccdfnames_ds.py
Final version created on Sat 02 Aug 2025
@author: Ed Tedesco

Purpose: To extract filenames from lois_none (f-formatted) images recovered from
         tape for ALL *.fits files with double-spaced headers in the executing
         directory. There were 4,278 such images from nights 980226 through
         981115, twenty of which were unusable.

Input:  Recovered image files in format f1234567.fits, f12345678.fits, and/or
        f123456789.fits in the same directory as create_ccdfnames_ds.py and
        images with double-spaced headers containing keywords DATE-UT and
        CCDPICNO. In addition, DATE-UT has 'YY/MM/DD in columns 11-19
        and CCDPICNO values (n through nnn) on line 39 in columns 28-30.
        
Output: Replaces the input f-formatted image filenames with the filenames
        required by the lois_none double-spaced pipeline:
        create_pds_files_none_ds.sh.
        and
        renamed_ds_lois_none_images.txt - A file with the recovered lois_none
        double-spaced filenames and the filenames constructed from their
        headers.
        This allows each lois_none image, e.g., 981114_001.fits, to be traced
        back to its source image, in this case, f0000004.fits.

Note: This variant is ONLY for lois_none f-formated images with double-spaced
      headers.

"""
#
import time
import os
import fnmatch
import astropy.io.fits
#
def Read_LONEOS_FITS():
#
# From https://stackabuse.com/python-list-files-in-a-directory/
# Lists all FITS files in the executing directory and writes them,
# and their headers to header.txt on alternate lines
# Requires import os, fnmatch
#
    listoffiles = os.listdir('.')
    pattern = "*.fits"
    for entry in listoffiles:
        if fnmatch.fnmatch(entry, pattern):
#            print (entry)
            hdulist = astropy.io.fits.open(entry)
#           The next line reads the DATE-UT keyword on header line 45 DATE_UT_startline            
            header1 = hdulist[0].header[DATE_UT_startline:DATE_UT_line]
            DATE_UT = hdulist[0].header[11:19]
            header2 = hdulist[0].header[CCDPICNO_startline:CCDPICNO_line]
            CCDPICNO = hdulist[0].header[28:30]
#            print(header2)
            global total
            total = total + 1
            DATE_UT = str(header1[0:DATE_UT_line])
            CCDPICNO = str(header2[0:CCDPICNO_line])
            CCDPICNO_out = CCDPICNO[27:30].strip()
            if len(CCDPICNO_out) == 1: CCDPICNO_out = '00'+CCDPICNO_out
            if len(CCDPICNO_out) == 2: CCDPICNO_out = '0'+CCDPICNO_out            
#
            with open('renamed_ds_lois_none_images.txt', mode='a') as file_object:
               DATE_UT_out = DATE_UT[11:13]+DATE_UT[14:16]+DATE_UT[17:19]
               print(DATE_UT_out+'_'+CCDPICNO_out+'.fits',entry,file=file_object)                
               new_file_name = DATE_UT_out+'_'+CCDPICNO_out+'.fits'
               os.replace(entry, new_file_name)
# End def Read_LONEOS_FITS()
#
# Main program starts below
#
# Start the script execution time counter
start_time = time.process_time()
#
total = 0
#
DATE_UT_line = 23
DATE_UT_startline = DATE_UT_line - 1

CCDPICNO_line = 20
CCDPICNO_startline = CCDPICNO_line - 1
#
Read_LONEOS_FITS()

print(' ')
execution_time = time.process_time() - start_time
execution_time = f'{float(execution_time):.3f}'
print ('Time to process',total,'images was', execution_time, "seconds")

