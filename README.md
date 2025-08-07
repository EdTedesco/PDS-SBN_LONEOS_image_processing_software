Pipeline: create_pds_files_none_ds.sh

This script ONLY WORKS FOR IMAGES WITHOUT A LOIS VERSION, i.e., lois_none
AND WITH A DOUBLE-SPACED HEADER!

This script creates augmented images and PDS4 Labels for LONEOS-I image files
with double-spaced headers and must be run from within an Ubuntu montage38 
terminal in D:\LONEOS\wd via the command: bash create_pds_files_none_ds.sh

Actions on bias files are not performed because none of the lois_none nights
have bias images.

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

D:\LONEOS\wd\_1\
D:\LONEOS\wd\_1a\
&nbsp;&nbsp;&nbsp;&nbsp;D:\LONEOS\wd\_1a\hdr\
&nbsp;&nbsp;&nbsp;&nbsp;D:\LONEOS\wd\_1a\wcs_hdr\
D:\LONEOS\wd\_2\
D:\LONEOS\wd\_2a\
&nbsp;&nbsp;&nbsp;&nbsp;D:\LONEOS\wd\_2a\hdr\
&nbsp;&nbsp;&nbsp;&nbsp;D:\LONEOS\wd\_2a\wcs_hdr\
D:\LONEOS\wd\bias\
D:\LONEOS\wd\hdr\
D:\LONEOS\wd\none\
&nbsp;&nbsp;&nbsp;&nbsp;D:\LONEOS\wd\none\hdr\  
&nbsp;&nbsp;&nbsp;&nbsp;D:\LONEOS\wd\none\wcs_hdr\

Output directories:

D:\LONEOS\_LONEOS_Archive\data_augmented\lois_none
D:\LONEOS\_LONEOS_Archive\data_original\lois_none
D:\LONEOS\_LONEOS_Archive\intermediate_files\lois_none

Not all pipeline use all of the above directories. After running, each pipeline
deletes the files it created in these directories thereby returning them to the
state required for the next run.

This script will load the (montage38) eft@Metis:/$ environment required to use
MontagePy modules.

The steps required to do this are:

0) This step is done before this script is run and consists of viewing the
images to be processed, renaming any that do not have the correct .fits
format, discarding any corrupt ones found, and copying those to be processed
to directory D:\LONEOS\wd\

1) Start Ubuntu in Run as Admin mode and enter: cd /mnt/d/LONEOS/wd followed by
   'bash pipeline_specific_script.sh'

2) This will run the following codes from the indicated lines and directories,
   using pipeline create_pds_files_none_ds.sh as an example. The specific
   scripts to run are detailed in each pipelines .sh script.

   158 python create_org_fits_files_none\_ds.py from D:\LONEOS\wd
   166 python create_hdr_none_ds.py
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
