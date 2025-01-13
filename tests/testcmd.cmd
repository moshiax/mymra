@echo off

set marker=ITSTEST
set password=COCKER
set errors=0

:: Embedding a file
mymra embed 123.mp4 123.png 1488.png -p %password% -m %marker%
if %errorlevel% neq 0 (
    echo [ERROR] Embedding a file - Failed!
    set /a errors+=1
) else (
    echo [SUCCESS] Embedding a file - Successful
)

:: Analyzing a file containing embedded file
mymra analyze 1488.png -p %password% -m %marker%
if %errorlevel% neq 0 (
    echo [ERROR] Analyzing a file containing embedded file - Failed!
    set /a errors+=1
) else (
    echo [SUCCESS] Analyzing a file containing embedded file - Successful
)

:: Extracting a file
mymra extract 1488.png -p %password% -m %marker%
if %errorlevel% neq 0 (
    echo [ERROR] Extracting a file - Failed!
    set /a errors+=1
) else (
    echo [SUCCESS] Extracting a file - Successful
)

:: Embedding a string
mymra embed_string "This is a secret string" 123.png string_embedded.png -p %password% -m %marker%
if %errorlevel% neq 0 (
    echo [ERROR] Embedding a string - Failed!
    set /a errors+=1
) else (
    echo [SUCCESS] Embedding a string - Successful
)

:: Analyzing a file containing embedded string
mymra analyze string_embedded.png -p %password% -m %marker%
if %errorlevel% neq 0 (
    echo [ERROR] Analyzing a file containing embedded string - Failed!
    set /a errors+=1
) else (
    echo [SUCCESS] Analyzing a file containing embedded string - Successful
)

:: Extracting a string
mymra extract_string string_embedded.png -p %password% -m %marker%
if %errorlevel% neq 0 (
    echo [ERROR] Extracting a string - Failed!
    set /a errors+=1
) else (
    echo [SUCCESS] Extracting a string - Successful
)

:: Removing embedded data
mymra deembed 1488.png cleaned_123.png -m %marker%
if %errorlevel% neq 0 (
    echo [ERROR] Removing embedded data - Failed!
    set /a errors+=1
) else (
    echo [SUCCESS] Removing embedded data - Successful
)

del /f /q cleaned_123.png 2>nul
del /f /q 1488.png 2>nul
del /f /q string_embedded.png 2>nul

if %errors% neq 0 (
    echo [ERROR] Test completed with %errors% errors.
    exit /b 1
) else (
    echo [SUCCESS] Test completed successfully.
    exit /b 0
)
