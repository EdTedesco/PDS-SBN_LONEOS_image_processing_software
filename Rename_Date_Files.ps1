# Renames YYMMDD_nnn.fits to YYMMDDa_nnn.fits
Get-ChildItem -Filter '*.fits' | ForEach-Object {
    
#   $newName = $_.BaseName + $suffix + $_.Extension
    $newName = ($_.name -replace '_','a_')	
    Rename-Item -path $_ -NewName $newName
}
exit
