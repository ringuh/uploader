from config import conf
print(conf)

import paramiko
k = paramiko.RSAKey.from_private_key_file(conf["key"])
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect( hostname =conf["server"], username=conf["user"], pkey=k )

sftp = c.open_sftp()
sftp.put('testi.key', '/home/picuploader/file.ext')
c.close()

# from ftplib import FTP_TLS
# ftps = FTP_TLS('pienirinkula.com', "root", keyfile="pub_ssh.key")
# ftps.login()
# ftps.prot_p()
# ftps.nlst()