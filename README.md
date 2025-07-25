TBD
See branch https://github.com/EdTedesco/PDS-SBN_LONEOS_image_processing_software/tree/Renaming_f-formatted_ss_images for a script to rename single-spaced f-formatted images recovered from backup tapes.

This is a python script to extract filenames from Lowell Observatory Near-Earth Object Survey (LONEOS) images recovered from backup tapes 006_CR through 012_CR for all such Flexible Image Transport System (FITS) files with double-spaced headers. There are 26 nights with 4,278 images between 1998/02/26 through 1998/11/15, inclusive, for which such data exist all of which have double-spaced (ds) headers. 

Recovered images are those that could not be read from the backup tapes using normal tape reading tools and which were extracted by Datarecovery.com, Inc.® (DR) using their “… program to essentially comb though the raw compressed data looking for FITS file markers …”. The format DR used for images it recovered from tapes that could not be read using normal tape-reading tools was of the form f123456789.fits and which are referred to in the Archive documentation as "f-formatted" files.

See loneos_processing_details_v2.pdf in the (not yet released at the time of this writing) Planetary Data System / Small Bodies Node (PDS/SBN) V2.0 Archive  https://sbn.psi.edu/pds/resource/loneos.html for the details (this link will take you to the V1.0 Archive which does not include these images and is included here as a placeholder). 

However, the PDS/SBN refused to allow this unmodified original data to be archived at the PDS/SBN and, due to the size of the dataset (~12TB), Zenodo was also unable to archive them. Consequently, unless this dataset becomes available elsewhere at some point this Python script has no images (other than the few example files included here) on which to run.

Nevertheless, because NASA requires all software developed under its support to be archived I am doing so here.

Dependencies include: 
time 
os 
fnmatch 
astropy.io.fits
