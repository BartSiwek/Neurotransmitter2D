@echo off

if "%1" == "" goto error

CALL triangulate.bat 30 0.0005 "..\..\Data\Meshes\%1.poly"
goto end

:error
echo ERROR: An argument is required

:end
