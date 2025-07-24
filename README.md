This is a python script to extract filenames from Lowell Observatory Near-Earth Object Survey (LONEOS) images recovered from backup tapes for all such Flexible Image Transport System (FITS) files with double-spaced headers.
See loneos_processing_details_v2.pdf in the (not yet released at thee time of writing this) https://sbn.psi.edu/pds/resource/loneos.html for the details (this link will take you to the V1.0 Archive which does not include these images). However, because 
Dependencies include:
time
os
fnmatch
astropy.io.fits
