#!/bin/bash
# Program: create_pds_files_none_ds.sh
<<PURPOSE

This script ONLY WORKS FOR IMAGES WITHOUT A LOIS VERSION, i.e., lois_none
AND WITH A DOUBLE-SPACED HEADER!

This script creates augmented images and PDS4 Labels for LONEOS-I image files
with double-spaced headers and must be run from within an Ubuntu montage38 
terminal in D:\LONEOS\wd\ via the command: . create_pds_files_none_ds.sh

Actions on bias files are not performed because none of the lois_none nights
with double-spaced headers have bias images.

The following codes and template files must be in the indicated directories:

Input:
In D:\LONEOS\wd The original renamed f-formatted .fits files (like
980425_001.fits), create_org_fits_files_none_ds.py, create_hdr_none_ds.py,
step_2_none.btm, Rename_LONEOS_Files.ps1 (used in step_2_none.btm),
step_3_none.btm, and step_6-7_none.btm and
In D:\LONEOS\wd\none add_wcs_none.py, create_wcs_hdr_none.py, and
create_label_none.py, plus template files YYMMDD.csv, YYMMDDa.csv,
YYMMDD.tbl, and YYMMDD_all.tbl 

Output: 
Original images (like 980425_001.fits in 980425.tar) and their Label files
(e.g., 980425.csv) in D:\LONEOS\_LONEOS_Archive\data_original\lois_none\980425.
Augmented images (like 980425a_001.fits in 980425a.tar) and their Label files
(e.g., 980425_a.csv) in D:\LONEOS\_LONEOS_Archive\data_augmented\lois_none\980425.
Intermediate files (980425.tbl, 980425_all.tbl, 980425_hdr.tar, 980425_wcs_hdr.tar,
and org_fits_files.txt) in D:\LONEOS\_LONEOS_Archive\intermediate_files\lois_none\980425.

The intermediate files are no longer needed after this code exits and so are
deleted from their working directories in step_6-7_none.btm

In addition to the above the following, empty, input and output directories
must exist prior to running the pipeline.

Input directories:

D:\LONEOS\wd\_1
D:\LONEOS\wd\_1a
   D:\LONEOS\wd\_1a\hdr
   D:\LONEOS\wd\_1a\wcs_hdr
D:\LONEOS\wd\_2
D:\LONEOS\wd\_2a
   D:\LONEOS\wd\_2a\hdr
   D:\LONEOS\wd\_2a\wcs_hdr
D:\LONEOS\wd\bias
D:\LONEOS\wd\hdr
D:\LONEOS\wd\none\
   D:\LONEOS\wd\none\hdr
   D:\LONEOS\wd\none\wcs_hdr

Output directories:

D:\LONEOS\_LONEOS_Archive\data_augmented\lois_none
D:\LONEOS\_LONEOS_Archive\data_original\lois_none
D:\LONEOS\_LONEOS_Archive\intermediate_files\lois_none

This pipeline does not use all of the above directories, e.g., D:\LONEOS\wd\bias
or their contents but others do. After running, each pipeline deletes the files
it created in these directories thereby returning them to the state required for
the next run.

This script will load the (montage38) eft@Metis:/$ environment required to use
MontagePy modules.

The steps required to run this pipeline are:

0) This step is done before the pipeline is run and consists of viewing the
images to be processed, renaming any that do not have the YYMMDD_nnn.fits
format, discarding any corrupt ones found, and copying those to be processed
to directory D:\LONEOS\wd\

1) Start Ubuntu in Run as Admin mode and enter: cd /mnt/d/LONEOS/wd followed
by 'bash create_pds_files_none_ds.sh'

2) This will run the following codes from the indicated lines and directories.

158 python create_org_fits_files_none_ds.py from D:\LONEOS\wd
166 python create_hdr_none_ds.py from D:\LONEOS\wd
204 '/mnt/c/Program Files/JPSoft/TCMD29/tcc.exe' step_2_none.btm from D:\LONEOS\wd
222 '/mnt/c/Program Files/JPSoft/TCMD29/tcc.exe' step_3_none.btm from D:\LONEOS\wd
264 python add_wcs_none.py from D:\LONEOS\wd\none
269 python create_wcs_hdr_none.py from D:\LONEOS\wd\none
365 python create_label_none.py from D:\LONEOS\wd\none 
421 '/mnt/c/Program Files/JPSoft/TCMD29/tcc.exe' step_6-7_none.btm from D:\LONEOS\wd

Before step_3_none.btm is run the code pauses to allow the user to see if all
the original .fits images in D:\LONEOS\wd were renamed and moved to ...\wd\none
If they were not, then the user can manually rename and move them.

In addition to the above some file management tasks (rm, mv, mkdir) are performed
within the bash script and the following template files must be in D:\LONEOS\wd\none
YYMMDD.csv, YYMMDD.tbl, YYMMDD\_all.tbl, and YYMMDDa.csv

As noted above, most intermediate files used to create the labels are deleted,
thus readying the directories for the next night's original images to be
processed into augmented images and their labels.

PURPOSE
# 
# ********** Define Functions **********
function pause() {
   read -p "$*"
}
#
# Function to return the total number of images in D:\LONEOS\wd
# Requires org_fits_files.txt to be present in D:\LONEOS\wd
#
function num_images(){
num_images="$(grep -c _ org_fits_files.txt)"
}
#
# Function to check whether the names of the images to be processed are in
# the standard .fits format (YYMMDD_nnn.fits) or the Lowell observatory
# LOIS's format (YYMMDD.nnn). 

# If they are in the standard format the images remain in D:\LONEOS\wd\_1.
# The pipeline then continues without running Rename_LONEOS_Files.ps1

# Input: Original images to be processed in directory D:\LONEOS\wd\_1

# Output: Original images, in standard format, in directory D:\LONEOS\wd\_1
#         and the number of images in variable num_images
# 
#           ----------------- Functions -----------------
# 
# Function to return the number of header (.hdr) files in directory
# D:\LONEOS\wd\hdr This should be the same as the number of images 
# 
function num_hdr(){
   shopt -s nullglob dotglob
   matched_files=(/mnt/d/LONEOS/wd/hdr/*.hdr)
   if ! (( ${#matched_files[*]} )); then
     num_hdr=${#matched_files[@]}
#     echo "Directory D:\\LONEOS\\wd\\hdr contains $num_hdr items"
   else
     num_hdr=${#matched_files[@]}
#     echo "Directory D:\\LONEOS\\wd\\hdr contains $num_hdr items"
   fi
   shopt -u nullglob dotglob
}
# 
# Function to Produce Modified Table 1
# This function requires YYMMDD_all.tbl to be in
# /mnt/d/LONEOS/wd/none
# 
function modify_table_1(){
cd /mnt/d/LONEOS/wd/none
# pause "Check if YYMMDD_all.tbl is in /wd/none then press [Enter] to resume ..."
declare -i n=1
file_in="/mnt/d/LONEOS/wd/none/$table_1_all"
file_out="/mnt/d/LONEOS/wd/none/$table_1"
# rm $file_out # Delete file_out if it already exists
while IFS= read -r -u9 line; do
if [ $n -gt 3 ]
then
   echo $n
   echo "$line" >> $file_out
#   pause "Press [ENTER] to resume ..."
fi
n=n+1
done 9< $file_in
}
# ********** End of function definitions **********
# 
conda activate montage38
# 
# Create the LONEOS Archive directories for the files produced by this script
#
# The following directories already exist: 
# 
# D:\LONEOS\_LONEOS_Archive\intermediate_files 
# D:\LONEOS\_LONEOS_Archive\data_augmented
# D:\LONEOS\_LONEOS_Archive\data_original
# 
#
# ls -1 ??????_???.fits > files.txt
# obs_night=$(head -c 6 files.txt)
# rm files.txt
# archive_int11="/mnt/d/LONEOS/_LONEOS_Archive/intermediate_files/"
# new_archive_dir_int="$archive_int11$obs_night"
# mkdir -p $new_archive_dir_int
# echo 'Created intermediate_files Archive Directory for $obs_night'
# pause 'from create_pds_files_none_ds.sh line 143. Press [ENTER] to continue...'
#
clear
# echo 'The purpose of Steps 1 and 2 is to create the standard filename images'
# echo 'including their PDS4 Labels.'
# echo
# pause 'Press [ENTER] to continue...'
# 
# echo " "
SECONDS=0
cd /mnt/d/LONEOS/wd
#
# Create org_fits_files.txt
# pause 'About to run python create_org_fits_files_none_ds.py'
python create_org_fits_files_none_ds.py
cp org_fits_files.txt /mnt/d/LONEOS/wd/none # /org_fits_files.txt
num_images
echo 'Now on line 160 of create_pds_files_none_ds.sh'
echo 'num_images =' $num_images
echo 'num_images =' $num_images, ' num_hdr =' $num_hdr
# pause 'About to run python create_hdr_none_ds.py'
# pause "Press [ENTER] to resume ..."
python create_hdr_none_ds.py
num_hdr
# pause 'shLine 166 After running python create_hdr_none_ds.py'
rm /mnt/d/LONEOS/wd/hdr/*.hdr      # Deletes any *.hdr from ...wd/hdr
# cp *.hdr /mnt/d/LONEOS/_LONEOS_Archive/_Temp/hdr
cp *.hdr /mnt/d/LONEOS/wd/none/hdr # Copies *.hdr from ...wd to ...wd/none/hdr
mv *.hdr /mnt/d/LONEOS/wd/hdr      # Moves *.hdr from ...wd to ...wd/hdr 
echo ' '
echo 'Now on line 172 of create_pds_files_none_ds.sh'
echo 'At this point the header files for the FITS files to be'
echo 'processed have been created in D:\LONEOS\wd\hdr.'
echo 'num_images =' $num_images, 'num_hdr =' $num_hdr
echo ' '
echo 'Completed Step 1 - Created the list of .fits files to be augmented'
echo '(org_fits_files.txt in D:\LONEOS\wd) and their single-spaced header'
echo 'files (as YYMMDD_nnn.hdr) in D:\LONEOS\wd\hdr.'
echo ' '
echo 'The number of .hdr files should equal the number of images.'
echo 'If they are not equal, that will be reported here.'
echo 'This is line 183 of create_pds_files_none_ds.sh'
# pause 'Press [ENTER] to resume ...'
# if [[ $num_hdr -ne $num_images ]]
# then
#   echo 'There are different numbers of hdr and fits files in D:\LONEOS\wd\hdr'
#   pause "Press [ENTER] to resume ..."
# # else
# #  echo 'There were the same number of hdr and fits files in D:\LONEOS\wd\hdr'
# #  pause "Press [ENTER] to resume ..."
# fi
# 
# Step 2 - Create tar files of the original images.
# Before running step_2.btm change to the directory where it is located
#
cd /mnt/d/LONEOS/wd
# echo ' '
# echo 'num_images =' $num_images
# echo ' '
# pause "shLine 201. Press [ENTER] to run step_2_none.btm ..."
'/mnt/c/Program Files/JPSoft/TCMD29/tcc.exe' step_2_none.btm
# 
# echo ' '
# echo 'Completed Step 2: Created tar files of the original images in'
# echo 'directory D:\LONEOS\_LONEOS_Archive\data_original\lois_none as'
# echo 'YYMMDD.tar using step_2.btm under TCC.'
# echo num_1_images= $num_1_images num_2_images= $num_2_images and num_images= $num_images
# echo ' '
# pause "Press [ENTER] to continue with Step 3 ..."
# 
# Step 3 - Create cropped versions of the original images
# At the start of this step we are in directory /mnt/d/LONEOS/wd from which
# step_3_none.btm is then called to crop all the original .fits images
# in this directory.
# 
echo Now on line 219 of create_pds_files_none_ds.sh
# pause 'Press [ENTER] to run step_3_none.btm ...'
cd /mnt/d/LONEOS/wd
'/mnt/c/Program Files/JPSoft/TCMD29/tcc.exe' step_3_none.btm
#
# #echo ' '
# #echo 'From line 223 in create_pds_files_none_ds.sh:' 
# #echo 'Step 4 - Add WCS information to the cropped image files created by'
# #echo 'step_3_none.btm after first checking for stranded *.fits files,'
# #echo 'and then run add_wcs_none.py.'
# #pause 'Press [ENTER] to run Step 4 after checking for stranded *.fits files...'
cd /mnt/d/LONEOS/wd
sleep 2
# mv ??????a_???.fits /mnt/d/LONEOS/wd/none
# 
# echo ' '
# echo 'Line 233: Check for stranded .fits files - YYMMDD_nnn.fits in ../wd and'
# echo 'if found rename them to YYMMDDa_nnn.fits and move them to wd\none.' 
# pause 'Press [ENTER] to continue ...'
# for file in /mnt/d/LONEOS/wd/*.fits
# do
#   if [ -e "$file" ]
#   then
#     clear
#     echo 'Line 241 in create_pds_files_none_ds.sh -'
#     echo 'Manually rename any stranded image files to YYMMDDa_nnn.fits and then '
#     pause 'move them to the wd\none dir, and then Press [ENTER] to continue ...'
#     continue
#   else
#     continue
#   fi
# done
# 
cd /mnt/d/LONEOS/wd/hdr
sleep 1
echo ' '
echo 'Continuing to process images. (Please be patient...)'

# mv ??????a_???.hdr /mnt/d/LONEOS/wd/none/hdr
echo ' '
echo "Will next cd to /wd/none and run add_wcs_none.py from there."
# #pause "Press [ENTER] to continue ..."
# 
cd /mnt/d/LONEOS/wd/none
sleep 2
python add_wcs_none.py
sleep 5
#echo "From create_pds_files_none_ds.sh line 267:"
#pause "Returned from add_wcs_none.py Press [ENTER] to continue ..."
#
python create_wcs_hdr_none.py
sleep 5
echo "From create_pds_files_none_ds.sh line 269:"
echo "Returned from create_wcs_hdr_none.py"
#pause "sh273 Press [ENTER] to continue and do by hand."
obs_night=$(head -c 6 /mnt/d/LONEOS/wd/org_fits_files.txt) # e.g., 980425
mkdir -p /mnt/d/LONEOS/_LONEOS_Archive/intermediate_files/lois_none/$obs_night
cd /mnt/d/LONEOS/wd/none/wcs_hdr
cp *_wcs.hdr /mnt/d/LONEOS/_LONEOS_Archive/_Temp/wcs_hdr
echo "Copied *_wcs.hdr to ...\_LONEOS_Archive\_Temp\wcs_hdr using shline 276" 
#cd /mnt/d/LONEOS/wd/none/hdr
#mv *.hdr /mnt/d/LONEOS/_LONEOS_Archive/_Temp/hdr
mkdir -p /mnt/d/LONEOS/_LONEOS_Archive/intermediate_files/lois_none/$obs_night
cp /mnt/d/LONEOS/wd/org_fits_files.txt /mnt/d/LONEOS/_LONEOS_Archive/intermediate_files/lois_none/$obs_night
cd /mnt/d/LONEOS/wd/none
# echo "Moved org_fits_files.txt to ...\_LONEOS_Archive\intermediate_files\lois_none\$obs_night"
# echo "using shline 285"
# pause "in create_pds_files_none_ds.sh line 286. Press [ENTER] to continue ..."
#cd /mnt/d/LONEOS/wd/none
sleep 5
<<skip_step_4_msg
echo ' '
echo 'Completed Step 4 which'
echo 'Added WCS information to the cropped image files in ...wd/none using'
echo 'Python code add_wcs_none.py and moved their original .hdr files'
echo 'to _1a/hdr and the WCS .hdr files to ...wd/none/wcs_hdr.'
echo ' '
#
echo "From line 297 of create_pds_files_none_ds.sh"
echo "About to start Step 5. - Create PDS4 Labels"
#  pause "Press [ENTER] to continue ..."
skip_step_4_msg
# 
<<skip_step_5_msg
# Define string variables used in creating the .csv templates and
# the modified table files required by create_label_none.py 
# Only those used for these purposes are defined here.
bias_flag = 0
obs_night=$(head -c 6 /mnt/d/LONEOS/wd/org_fits_files.txt) # e.g., 980425
if [ $bias_flag -eq 0 ] # Since there are no bias files the dirs below
then                    # were not created so they are created here
   archive_aug_none="/mnt/d/LONEOS/_LONEOS_Archive/data_augmented/lois_none/"
   archive_org_none="/mnt/d/LONEOS/_LONEOS_Archive/data_original/lois_none/"
   archive_int_none="/mnt/d/LONEOS/_LONEOS_Archive/intermediate_files/"
	 new_archive_dir_aug="$archive_aug_none$obs_night"
   new_archive_dir_org="$archive_org_none$obs_night"
   new_archive_dir_int="$archive_int_none$obs_night"
	 mkdir -p $new_archive_dir_aug
   mkdir -p $new_archive_dir_org
   mkdir -p $new_archive_dir_int
  #echo 'Output directories created.'
  #pause 'Press [Enter] to continue ...'
fi
skip_step_5_msg
#obs_night=$(head -c 6 /mnt/d/LONEOS/wd/org_fits_files.txt) # e.g., 980425
mkdir -p "/mnt/d/LONEOS/_LONEOS_Archive/data_augmented/lois_none/$obs_night"
#mkdir -p "/mnt/d/LONEOS/_LONEOS_Archive/data_original/lois_none/$obs_night"
#mkdir -p "/mnt/d/LONEOS/_LONEOS_Archive/intermediate_files/lois_none/$obs_night"
echo 'shLine 325: Current night output directories created and the *a_wcs.hdr files'
echo 'are copied to D:\LONEOS\_LONEOS_Archive\intermediate_files\lois_none\YYMMDD'
cd /mnt/d/LONEOS/_LONEOS_Archive/_Temp/wcs_hdr
cp *_wcs.hdr /mnt/d/LONEOS/_LONEOS_Archive/intermediate_files/lois_none/$obs_night
cd /mnt/d/LONEOS/wd/none
# #pause 'create_pds_files_none_ds.sh Line 330: Press [Enter] to continue ...'
csv1=".csv"
csv1a="a.csv"
night_csv1="$obs_night$csv1"
night_csv1a="$obs_night$csv1a"
tbl_all="_all.tbl"
tbl_1=".tbl"
table_1_all="$obs_night$tbl_all"
table_1="$obs_night$tbl_1"
echo ' '
echo "shLine 340: table_1 =" $table_1
# #pause "Press [ENTER] to continue ..."
echo ' '
echo 'shLine 343: Step 5a - Completed defining string variables used in creating'
echo 'the .csv templates and the modified table files required by'
echo 'create_label_none.py, which runs from directory ...wd/none.'
echo ' '
# #pause "Press [ENTER] to continue ..."
echo ' '
# #pause 'shLine 349: Step 5b - Modify .csv & .tbl Files section of Create PDS4 Labels'
cd /mnt/d/LONEOS/wd/none
cp YYMMDD.csv $night_csv1
sleep 3
cp YYMMDDa.csv $night_csv1a
sleep 3
modify_table_1 # The following two lines could replace modify_table_1. This  
#                assumes the template files YYMMDD_all.tbl and YYMMDD.tbl 
#                are in /mnt/d/LONEOS/wd/none 
#cp YYMMDD_all.tbl $obs_night$tbl_all
#cp YYMMDD.tbl $obs_night$tbl_1
sleep 3
# echo 'Now on line 361 of create_pds_files_none_ds.sh in /wd and will next run'
# pause 'create_label_none.py from /wd/none Press [ENTER] to continue ...'
python create_label_none.py
echo 'Returned from create_label_none.py to create_pds_files_none_ds.sh line 364:'
# pause 'Press [ENTER] to continue ...'
mv $night_csv1 /mnt/d/LONEOS/_LONEOS_Archive/data_original/lois_none/$obs_night
mv $night_csv1a /mnt/d/LONEOS/_LONEOS_Archive/data_augmented/lois_none/$obs_night
mv $obs_night$tbl_all /mnt/d/LONEOS/_LONEOS_Archive/intermediate_files/lois_none/$obs_night
mv $obs_night$tbl_1 /mnt/d/LONEOS/_LONEOS_Archive/intermediate_files/lois_none/$obs_night
# echo 'create_pds_files_none_ds.sh line 370: Returned from create_label_none.py'
# pause 'Press [ENTER] to continue ...'
# 
# echo ' '
# echo 'From line 374 of create_pds_files_none_ds.sh' 
# echo 'Step 5 - Completed creation of PDS4 .csv Label files.'
# echo 'Label files YYMMDD.csv, and YYMMDDa.csv are now in D:\LONEOS\wd\none'
# pause "Finished Step 5. Press [ENTER] to resume ..."
# 
# *****************************************************************************
# SKIP
# 
# Step 6 - Create the YYMMDD LONEOS Archive directories for LOIS none -
# D:\LONEOS\_LONEOS_Archive\data_original\lois_none\YYMMDD and
# D:\LONEOS\_LONEOS_Archive\data_augmented\lois_none\YYMMDD and moving
# the original and augmented files and their label files into them
# for delivery to the PDS.
# 
# The tared files for the original .fits images have already been
# created and moved to dir ...wd/_1 in Step 2, above, and their .fits
# files deleted. Therefore, in this Step we must do the same for the
# augmented fits images currently in dir ...wd/none.
# 
# The date for the files currently being processed are obtained from
# org_fits_files.txt in dir /mnt/d/LONEOS/wd (aka D:\LONEOS\wd).
# 
# Create YYMMDDa.tar from the .fits files in dir ...wd/none
# 
# echo ' '
# echo Step 6 creates tar archives of, and then moves, the processed .fits and
# echo Label files into their appropriate archive directories. This is being
# echo done in a .btm script because the Windows tar function runs 4-times
# echo faster than the tar function run under Ubuntu.
# echo ' '
# echo The original .fits files have already been archived to tar files in
# echo D:\\LONEOS\\wd\\1 in Step 2.
# echo ' '
# echo The augmented .fits files in D:\\LONEOS\\wd\\none will be archived to
# echo tar files and moved into their appropriate archive directories by this
# echo script for delivery to the PDS.
# echo ' '
# echo Step 7 saves all the intermediate files used in creating the augmented
# echo images and their labels.
# echo ' '
# 
cd /mnt/d/LONEOS/wd
# echo "create_pds_files_none_ds.sh Line 416: obs_night = $obs_night"
# pause "Press [ENTER] to run step_6-7_none.btm ..."
sleep 2
'/mnt/c/Program Files/JPSoft/TCMD29/tcc.exe' step_6-7_none.btm
# pause "Returned from step_6-7_none.btm Press [ENTER] to continue ..."
# 
clear
echo ' '
echo "The number of images processed for night $obs_night was $num_images:"
echo "and the elapsed time for running these images was: $SECONDS seconds."
echo ' '
echo 'FINIS'
# echo ' '
# echo "Pressing [ENTER] will exit the script and return to the \
# Ubuntu terminal prompt."
# pause "Press [ENTER] to exit ..."
# echo ' '