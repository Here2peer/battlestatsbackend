@echo off
ECHO.
ECHO.
ECHO.

SET file=Main.py

ECHO Default file is %file% press enter to use
ECHO.
SET /P file=File to use:
ECHO.
SET FLASK_APP=%file%
SET FLASK_ENV=development
flask run