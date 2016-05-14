# uploader
python script to be run in background.
requires python and web server to upload the images to.

will check selected folders every 15 seconds for new images and upload them on your server through SSH.
will add the link to the uploaded picture on your clipboard.

for windows create shortcut to Startup-folder for pythonw.exe.
example shortcut target:
C:\Users\<user>\AppData\Local\Programs\Python\Python35\pythonw.exe C:\Users\<user>\Documents\GitHub\uploader\run.py

