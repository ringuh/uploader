from config import conf
import paramiko, os, json, hashlib, pyperclip, threading, shutil
from tkinter import Tk

allowed = ["png", "jpg", "jpeg", "svg", "gif", "webm"]

script_path = os.path.dirname(os.path.realpath(__file__))

count = 0
def Loop():
	global script_path
	global allowed
	global conf


	files = []
	uploaded = []
	for folder in conf["target"]:
		# siirretään kuvat tähän kansioon uploadin jälkeen, varmistetaan, että kansio on olemassa
		copy_path = os.path.join(folder, "uploaded")
		try: os.stat(copy_path)
		except: os.mkdir(copy_path)

		# loopataan kaikki filut kansiosta, ignorataan alikansiot
		for (dirpath, dirnames, filenames) in os.walk(folder):
		    files.extend(filenames)
		    break

		# käydään läpi löydetyt hyväksytyllä päätteellä olevat tiedostot
		for fn in files:
			ext = fn.split(".")[-1]
			if not ext in allowed:
				continue
			fpolku = os.path.join(folder, fn)
			date_created = os.path.getmtime(fpolku)
			# generoidaan tiedostoille toivottavasti uniikki nimi
			m = hashlib.sha224(bytes("{}{}".format(fpolku, date_created), "utf-8")).hexdigest()

			uploaded.append(dict(
					path=fpolku,
					date_created=date_created,
					rename="{}.{}".format(m, ext),
					move=copy_path,
				))

	#json.dump(new_files, f)

	#f.close()



	k = paramiko.RSAKey.from_private_key_file(
			os.path.join(script_path, conf["key"])
		)
	c = paramiko.SSHClient()
	c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	c.connect( hostname =conf["server"], username=conf["user"], pkey=k )

	url = None

	sftp = c.open_sftp()
	for file in uploaded: # uploadataan
		sftp.put(file["path"], '{}/{}'.format(conf["base"], file["rename"]))
		url = "{}{}".format(conf["baseurl"], file["rename"])
		print("Uploaded:"+file["rename"])
		# ja siirretään toiseen kansioon
		shutil.move(file["path"], os.path.join(file["move"], file["rename"]))
	c.close()



	if url: # kopioidaan viimeisen uploadatun kuvan osoite clipboardille
		pyperclip.copy(url)

	global count
	# count += 1
	if count < 2:
		threading.Timer(15.0, Loop).start()

Loop()