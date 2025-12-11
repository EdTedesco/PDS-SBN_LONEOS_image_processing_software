create_ccdfnames_ss.py is a python script to extract filenames from Lowell Observatory Near-Earth Object Survey (LONEOS) images recovered from backup tapes 012_CR through 043_CR for all such Flexible Image Transport System (FITS) files with single-spaced headers. There are 66 nights with 15,396 images between 1998/11/16 and 2000/01/11, inclusive, for which such data exist and all of which have single-spaced (ss) headers.

The following three paragraphs are from “§2.1.2 Renaming Files” in [loneos_processing_details_v2.pdf](https://sbnarchive.psi.edu/pds4/surveys/gbo.ast.loneos.survey/document/loneos_processing_details_v2.pdf), beginning immediately after Fig. 3:

“_The majority of the LONEOS-I images were extracted from the_ _CR tapes in the f-format[^1] using the recovery method described in Appendix I and hence could not be renamed as simply as those with the YYYYMMDDnnnnb.fits format. However, the original filenames of the f-formatted images could be reconstructed from keywords in their headers, e.g., the LONEOS-I images (those with dates through 2000/01/11), like f1053773.fits for example, had keywords “CCDPICNO=   22 / running sequence number” and “DATE-UT = '98/05/25   ' / ut date of obs”. Hence, f1053773.fits could be renamed 980525_022.fits_

_This process was automated by writing Python scripts which renamed the recovered filenames for ALL the *.fits files in the executing directory to their standard archive format for LONEOS-I images, i.e., YYMMDD_nnn.fits._ 

_Separate scripts were written to process the images with single-spaced and double-spaced headers. See  footnote a to Appendix I for additional information on the types of source-specific (i.e., HDD or tape) directories created for each night and on how the images for input into the pipelines were recovered from the tapes._” 

The example images here are from tapes 012_CR (obtained on 1998/11/16) and 043_CR (obtained on 2000/01/05)

Recovered images are those that could not be read from the backup tapes using normal tape reading tools and which were extracted by Datarecovery.com, Inc.® (DR) using their “… _program to essentially comb though the raw compressed data looking for FITS file markers_ …”. The format DR used for images it recovered from tapes that could not be read using normal tape-reading tools was of the form f123456789.fits and which are referred to in the Archive documentation as "f-formatted" files.

See [loneos_processing_details_v2.pdf](https://sbnarchive.psi.edu/pds4/surveys/gbo.ast.loneos.survey/document/loneos_processing_details_v2.pdf) for additional details.

Due to the size of the original dataset (~12TB), neither the PDS/SBN nor Zenodo were able to archive it online, _i.e._, none of the f-formatted files are available. Consequently, I've only uploaded a few example images to this branch to enable this Python script to run. At the time of this writing (12 Dec 2025) the PDS/SBN is working on whether, and if so, how to make all the original LONEOS image files available.

Required Python dependencies are: time, os, fnmatch, astropy.io.fits

[^1]: The format, _e.g._, f123456789.fits (where the numeric part had between seven and nine digits), Datarecovery.com, Inc.® (DR) used for images it recovered from tapes that could not be read using normal Unix tape-reading tools.
