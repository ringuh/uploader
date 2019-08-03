# uploader

requires python and web server to upload the images to.

<img src="/static/toast_example.png"/>

will check your selected folder every 5 seconds for new files and uploads them on your server through SSH.
will prompt you with windows toast after upload to add the URL on your clipboard


create virtualenv and install the requirements.txt
create a shortcut to startup-folder where source is:
"C:\Users\mypc\Envs\venv\Scripts\pythonw.exe C:\source_of_\uploader\run.py"

ssh connection will requires using private-key without password

conf = dict(
	user="your_unix_login",
	base="/var/www/<upload_folder>/",
	server="your.server",
	
	key="private.key",
	baseurl="https://your.server/",
	target="D:\\<source_folder_on_your_windows_pc>",
	toastExpiration=10000,
)
