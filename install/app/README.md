# app
This folder contains subfolders named after each character's NFC ID (hex code).
Some notes:
* Each subfolder will contain a shell script which launches some kind of app
(usually an emulator program).
* Non-supported Amiibo figures simply do not have a subfolder with their
hex code. See `Adding Apps to amiibrOS` below for information on how to add
apps for your Amiibo figures.

# Adding Apps to amiibrOS
1. Check this database for the hex code belonging to your amiibo figurine: https://docs.google.com/spreadsheets/d/19E7pMhKN6x583uB6bWVBeaTMyBPtEAC-Bk59Y6cfgxA/htmlview# . Column "C" (in green) contains the code you want.
2. Add a folder with the hex code obtained in step 1 underneath the app folder.
3. Write a shell script (.sh) which launches whatever app you want. Give the shell script the exact name you gave the folder in step 2, and place it underneath that folder.