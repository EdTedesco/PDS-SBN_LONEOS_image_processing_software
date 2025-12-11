This is a python script to extract filenames from Lowell Observatory Near-Earth Object Survey (LONEOS) images recovered from backup tapes 006_CR through 012_CR for all such Flexible Image Transport System (FITS) files with double-spaced headers. There are 26 nights with 4,278 images between 1998/02/26 through 1998/11/15, inclusive, for which such data exist all of which have double-spaced (ds) headers. 

Recovered images are those that could not be read from the backup tapes using normal tape reading tools and which were extracted by Datarecovery.com, Inc.® (DR) using their “… program to essentially comb though the raw compressed data looking for FITS file markers …”. The format DR used for images it recovered from tapes that could not be read using normal tape-reading tools was of the form f123456789.fits and which are referred to in the Archive documentation as "f-formatted" files.

See [loneos_processing_details_v2.pdf](https://sbnarchive.psi.edu/pds4/surveys/gbo.ast.loneos.survey/document/loneos_processing_details_v2.pdf) for the details. 

However, due to the size of the original dataset (~12TB), neither the PDS/SBN nor Zenodo were able to archive it online. Consequently, I've only uploaded a few example images to this branch to test this Python script. At the time of this writing (02 Aug 2025) the PDS/SBN is working on how to make all the original LONEOS image files available. 

Required Python dependencies are: 
time 
os 
fnmatch 
astropy.io.fits
