@echo off

if "%1" == "" goto error
if "%2" == "" goto error
if "%3" == "" goto error

"..\bin\traingle\triangle.exe" -pq%1A-a%2 "%3"
goto end

:error
echo ERROR: Three arguments required

:end
