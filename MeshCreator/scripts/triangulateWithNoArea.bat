@echo off

if "%1" == "" goto error

CALL triangulate.bat 20 1.0 "..\..\Data\Meshes\%1.poly"
goto end

:error
echo ERROR: An argument is required

:end
