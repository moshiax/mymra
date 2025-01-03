@echo off

:: Define the marker
set marker=ITSTEST

:: Embedding a file
mymra embed 123.mp4 123.png 1488.png -p COCKER -m %marker%
if %errorlevel% neq 0 (
    echo Embedding a file - Failed!
) else (
    echo Embedding a file - Successful
)

:: Extracting a file
mymra extract 1488.png -p COCKER -m %marker%
if %errorlevel% neq 0 (
    echo Extracting a file - Failed!
) else (
    echo Extracting a file - Successful
)

:: Embedding a string
mymra embed_string "This is a secret string" 123.png string_embedded.png -p COCKER -m %marker%
if %errorlevel% neq 0 (
    echo Embedding a string - Failed!
) else (
    echo Embedding a string - Successful
)

:: Extracting a string
mymra extract_string string_embedded.png -p COCKER -m %marker%
if %errorlevel% neq 0 (
    echo Extracting a string - Failed!
) else (
    echo Extracting a string - Successful
)

:: Removing embedded data
mymra deembed 1488.png cleaned_123.png -m %marker%
if %errorlevel% neq 0 (
    echo Removing embedded data - Failed!
) else (
    echo Removing embedded data - Successful
)

:: Clean up files
echo Cleaning up files...
del /f /q cleaned_123.png
del /f /q 1488.png
del /f /q string_embedded.png

echo Test completed.
