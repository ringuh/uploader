import zroya, time, os, hashlib, paramiko, pyperclip, shutil, datetime
from config import conf

#def onClickHandler(notification_id):
#def onActionHandler(notification_id, action_id):
#def onDismissHandler(notification_id, reason):
def GetStamp():
	return str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

f = open("loki.log", "w+")
f.write("Started:"+GetStamp())
f.close()

try:
	images = ["png", "jpg", "jpeg", "gif", "svg", "gif"]
	zroya.init("Uploader", "github.com/ringuh", "Uploader", "c", "v01")
	freeLoop = True

	def ErrorToast(e):
		te = zroya.Template(zroya.TemplateType.ImageAndText4)
		te.setFirstLine("Uploader Error:")
		te.setSecondLine(str(e))
		te.setImage("./prno.ico")
		te.setExpiration(30000)
		zroya.show(te)
		# record the error message
		f = open("loki.log", "w+")
		f.write("Error:" + GetStamp()+"\n"+str(e))
		f.close()


	def Toast(url, path, filename):
		def onActionHandler(notification_id, action_id):
			
			if action_id == 0:
				#print("copy to clipboard:", url)
				pyperclip.copy(url)

		t = zroya.Template(zroya.TemplateType.ImageAndText4)
		t.setFirstLine("Uploaded file:")
		t.setSecondLine(filename)
		
		# set the potential picture as Toast Icon
		t.setImage(path) if filename.split(".")[-1] in images else t.setImage("./static/prno.ico")
		t.setAudio(zroya.Audio.Call6)
			
		
		t.setExpiration(conf["toastExpiration"])
		t.addAction("Copy URL")
		t.addAction("Hide")
		zroya.show(t, on_action=onActionHandler)




	def Loop():
		files = []
		upload = []
		freeLoop = False

		folder = conf["target"]
		# check if the folder you are suppose to backup uploaded files to exists and create it if necessary
		copy_path = os.path.join(folder, "uploaded")
		try: os.stat(copy_path)
		except: os.mkdir(copy_path)
		

		# loop all files in folder, ignore other folders
		for (dirpath, dirnames, filenames) in os.walk(folder):
		    files.extend(filenames)
		    # break ignores subdirectories
		    break
		#print(files)

		for fn in files:
			ext = fn.split(".")[-1]
			file_path = os.path.join(folder, fn)
			date_created = os.path.getmtime(file_path)
			# generate random unique name for the file
			m = hashlib.sha224(bytes("{}{}".format(file_path, date_created), "utf-8")).hexdigest()
			upload.append(
				dict(
					path=file_path,
					rename="{}.{}".format(m, ext)
				)
			)
		
		if len(files) == 0:
			return True
		
		# find the SSH key from your project
		k = paramiko.RSAKey.from_private_key_file(
					os.path.join(os.path.dirname(os.path.realpath(__file__)), conf["key"])
				)
		
		c = paramiko.SSHClient()
		c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		c.connect( hostname=conf["server"], username=conf["user"], pkey=k )
		
		
		url = None

		sftp = c.open_sftp()
		for file in upload: # loop through files to upload
			sftp.put(file["path"], '{}/{}'.format(conf["base"], file["rename"]))
			url = "{}{}".format(conf["baseurl"], file["rename"])
			
			# move the file to backup folder after upload
			new_path = shutil.move(file["path"], os.path.join(copy_path, file["rename"]))

			# toast the URL for the last file or all files if its only a few of them
			if len(upload) < 4 or file == upload[-1]:
				Toast(url, new_path, file["rename"])
		c.close()
		return True

	while True: # keep the uploader active forever
		try:
			if freeLoop:				
				freeLoop = Loop()
				
		except Exception as e:
			ErrorToast(e)
			raise e
		
		time.sleep(5)


		

except Exception as e:
	ErrorToast(str(e)+"\nshutting down")
	raise e