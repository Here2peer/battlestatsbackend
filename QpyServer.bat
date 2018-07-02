@echo off
ECHO.
ECHO.
ECHO.

SET file=Main.py

ECHO Default file is %file%
ECHO.
ECHO.
SET FLASK_APP=%file%
SET FLASK_ENV=development
flask run --host=0.0.0.0
pause